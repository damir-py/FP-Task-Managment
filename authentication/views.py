from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from exceptions.CustomException import CustomException
from .models import User, Team, Task, Comment
from .serializers import UserSerializer, UserLoginSerializer, TokenSerializer, TeamSerializer, TaskSerializer, \
    TasksAddingSerializer, TeamAddingSerializer, CommentSerializer
from .utils import user_checking, create_background_task


class Authentication(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create User',
        operation_description='Create User',
        request_body=UserSerializer,
        responses={200: UserSerializer()},

        tags=['Authentication']
    )
    def create_user(self, request):
        data = request.data
        user = User.objects.filter(username=data.get('username')).first()
        if user and user.phone_number == data.get('phone_number'):
            return Response(data={'message': 'User already exists!', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        serializer_data = UserSerializer(user, data=data, partial=True) if user else UserSerializer(data=data)

        if not serializer_data.is_valid():
            return Response(data={'message': serializer_data.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        serializer_data.save()
        return Response(data={'message': serializer_data.data, 'ok': True})


class LoginView(ViewSet):
    @swagger_auto_schema(
        operation_summary='Login',
        operation_description='Login',
        request_body=UserLoginSerializer,
        responses={200: TokenSerializer()},
        tags=['Authentication']
    )
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(data={'message': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        user = user_checking(request.data)
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['role'] = user.role
        user.save()
        return Response(data={
            'result': {'access_token': str(access_token), 'refresh_token': str(refresh_token), 'role': user.role},
            'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Information about User',
        operation_description='Information about User',
        request_body=UserLoginSerializer,
        responses={200: UserSerializer()},
        tags=['Authentication']

    )
    def auth_me(self, request):
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            raise CustomException('User not found!')
        return Response({'message': UserSerializer(user, context={'request': request}).data, 'ok': False})


class TeamAndTaskAPIView(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create Team',
        operation_description='Create Team',
        request_body=TeamSerializer,
        responses={200: TeamSerializer()},
        tags=['Team and Task']
    )
    def team_create(self, request):
        team = Team.objects.filter(name=request.data.get('name')).first()
        if team:
            raise CustomException('Name already exists!')
        serializer = TeamSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'message': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data={'message': serializer.data, 'ok': True})

    @swagger_auto_schema(
        operation_summary='Create Team',
        operation_description='Create Team',
        request_body=TaskSerializer,
        responses={200: TaskSerializer()},
        tags=['Team and Task']
    )
    def task_create(self, request):
        task = Task.objects.filter(title=request.data.get('title')).first()
        if task:
            raise CustomException('Title already exists!')
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'message': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data={'message': serializer.data, 'ok': True})

    @swagger_auto_schema(
        operation_summary='Adding Tasks',
        operation_description='Adding Tasks',
        request_body=TasksAddingSerializer,
        responses={200: UserSerializer()},
        tags=['Adding']
    )
    def add_tasks(self, request):
        users_id = request.data.get('users_id')
        task_id = request.data.get('task_id')
        users = User.objects.filter(id__in=users_id)

        if not task_id or not users_id:
            raise CustomException('IDs are incorrect or not given!')
        task_obj = Task.objects.filter(id=task_id, team__user__in=users_id).first()
        if not task_obj:
            raise CustomException('Not valid tasks!')

        task_obj.user.add(*users)
        return Response(data={'message': TaskSerializer(task_obj).data, 'ok': True})

    @swagger_auto_schema(
        operation_summary='Adding Tasks',
        operation_description='Adding Tasks',
        request_body=TeamAddingSerializer,
        responses={200: UserSerializer()},
        tags=['Adding']
    )
    def add_team(self, request):
        user_id = request.data.get('users_id')
        team_id = request.data.get('team_id')

        if not team_id or not user_id:
            raise CustomException('IDs are incorrect or not given!')

        team_obj = Team.objects.filter(id=team_id).first()
        if not team_obj:
            raise CustomException('Not valid team!')
        user_obj = User.objects.filter(id=user_id).first()
        if not user_obj:
            raise CustomException('User not found!')
        team_obj.user = user_obj
        team_obj.save()

        return Response(data={'message': TeamSerializer(team_obj).data, 'ok': True})


class CommentAPIView(ViewSet):

    @swagger_auto_schema(
        operation_summary='Create comment to task',
        operation_description='Create comment to task',
        request_body=CommentSerializer(),
        responses={200: CommentSerializer()},
        tags=['comment']
    )
    def write(self, request, pk):
        user = User.objects.filter(id=request.user.id, task=pk).first()
        if not user:
            raise CustomException('User_id or Task_id not given correctly!')

        message = Comment.objects.create(task_id=pk, user_id=request.user.id, text=request.data.get('text'))
        message.save()
        serializer = CommentSerializer(message)

        return Response(data={'message': serializer.data, 'ok': True})


@api_view(['GET'])
def start_scheduler(request):
    from django.conf import settings
    if settings.SCHEDULER == 0:
        scheduler = create_background_task()
        scheduler.start()
        data = []
        for schedule in scheduler.get_jobs():
            data.append(schedule.next_run_time)
            settings.SCHEDULER = 1
        return Response(data={'result': data, 'ok': True}, status=status.HTTP_200_OK)
    raise CustomException('Scheduler already running!')
