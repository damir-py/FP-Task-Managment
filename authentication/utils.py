from pprint import pprint

from exceptions.CustomException import CustomException
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def user_checking(data):
    from .models import User
    user = User.objects.filter(username=data.get('username').lower()).first()
    if not user:
        raise CustomException('User not found!')
    if check_password(data.get('password'), user.password) is False:
        raise CustomException('Password or Username incorrect!')

    return user


def identify_role(token):
    token = token.split()[1]
    try:
        # Verify and decode the token
        payload = UntypedToken(token)
        print('token', payload)
        return payload

    except TokenError as e:
        return e
    except InvalidToken as e:
        return e
