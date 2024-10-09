from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import Team, Task, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone_number', 'role', 'team', 'created_at')
    list_display_links = ('id', 'username', 'phone_number')
    list_filter = ('team', 'role')

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')
        print(change)
        if password and not change or form.initial['password'] != password:
            obj.password = make_password(password)
        super().save_model(request, obj, form, change)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'deadline')
    list_display_links = ('id', 'title')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
