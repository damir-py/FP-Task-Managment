from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from exceptions.CustomException import CustomException
from .models import User, Team
from .serializers import UserSerializer, UserLoginSerializer, TokenSerializer, TeamSerializer
from .utils import user_checking


class Authentication(ViewSet):
    @swagger_auto_schema(
        operation_summary='Create User',
        operation_description='Create User',
        request_body=UserSerializer,
        responses={200: UserSerializer()},

        tags=['Authentication']
    )
    def create_user(self, request):
        print('ok')
        data = request.data
        user = User.objects.filter(username=data.get('username').lower()).first()
        if user:
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
        request_body=UserSerializer,
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
        tags=['Team']

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

    # def task_create(self, request):

