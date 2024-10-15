from datetime import date

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import UntypedToken

from exceptions.CustomException import CustomException


def user_checking(data):
    from .models import User
    user = User.objects.filter(username=data.get('username').lower()).first()
    if not user:
        raise CustomException('User not found!')
    if check_password(data.get('password'), user.password) is False:
        raise CustomException('Password or Username incorrect!')

    return user


def identify_role(token):
    if token:
        token = token.split()[1]

        payload = UntypedToken(token)
        return payload.get('role', '')


def create_background_task():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=11, minute=0, timezone=settings.TIME_ZONE)
    scheduler.add_job(deadline_checking, trigger=trigger)

    return scheduler


def deadline_checking():
    from .models import User, Task
    current_time = date.today()

    users = User.objects.exclude(role=1)
    tasks = Task.objects.filter(user__in=users).exclude(deadline__lt=current_time)
    if tasks:
        send_message(tasks)


def send_message(tasks):
    for task in tasks:
        message = """
    Project: Task managment\nTask name: {}\nDeadline given time: {}\nDeadline ends time: {}\n You have {}""".format(
            task.title, task.created_at, task.deadline, (task.deadline - date.today()))

    status = requests.get(settings.TELEGRAM_API_URL.format(settings.BOT_TOKEN, message, settings.CHANNEL_ID))
    if status.status_code != 200:
        raise CustomException("Texnik sabablarga ko'ra ko'd yuborilmadi, Iltimos keyinroq urinib ko'ring!")
