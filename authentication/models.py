from django.core.validators import RegexValidator
from django.db import models

from abstraction.base_model import BaseModel

USER_ROLE = (
    (1, 'Manager'),
    (2, 'User')
)


class User(BaseModel):
    username = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=14, unique=True, validators=[RegexValidator(regex='^\+998\d{9}$', )])
    password = models.CharField(max_length=100)
    role = models.IntegerField(choices=USER_ROLE, default=2)

    def __str__(self):
        return self.username


class Team(BaseModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Task(BaseModel):
    title = models.CharField(max_length=100)
    user = models.ManyToManyField(User, blank=True)

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)

    deadline = models.DateField()

    def __str__(self):
        return self.title


class Comment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.task.title
