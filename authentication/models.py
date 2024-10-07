from django.db import models
from abstraction.base_model import BaseModel

USER_ROLE = (
    (1, 'Manager'),
    (2, 'User')
)


class Team(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(BaseModel):
    title = models.CharField(max_length=100)

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title


class User(BaseModel):
    username = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=14)
    password = models.CharField(max_length=100)
    role = models.IntegerField(choices=USER_ROLE, default=2)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    tasks = models.ManyToManyField(Task)



    def __str__(self):
        return self.username
