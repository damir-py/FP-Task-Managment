from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import User


class Authentication(ViewSet):
    def create_user(self, request):
        data = request.data
        user = User.objects.filter(username=data.get('username', '').lower()).first()
        if user:
            return Response(data={'message': 'User already exists!', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

