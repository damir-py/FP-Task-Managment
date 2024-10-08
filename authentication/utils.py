from exceptions.CustomException import CustomException
from django.contrib.auth.hashers import check_password


def user_checking(data):
    from .models import User
    user = User.objects.filter(username=data.get('username').lower()).first()
    if not user:
        raise CustomException('User not found!')
    if check_password(data.get('password'), user.password) is False:
        raise CustomException('Password or Username incorrect!')

    return user
