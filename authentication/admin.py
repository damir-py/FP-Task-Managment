from django.contrib import admin

from .models import Team, Task, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone_number', 'role', 'team')
    list_display_links = ('id', 'username', 'phone_number')
    list_filter = ('team', 'role')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'deadline')
    list_display_links = ('id', 'title')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
