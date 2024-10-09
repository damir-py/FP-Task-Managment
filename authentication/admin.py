from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import Team, Task, User, Comment


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


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_filter = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at')
    list_display_links = ('id', 'text')
    list_filter = ('created_at',)


class CommentTabularInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'deadline', 'created_at')
    list_display_links = ('id', 'title')
    list_filter = ('created_at',)
    inlines = [CommentTabularInline]
