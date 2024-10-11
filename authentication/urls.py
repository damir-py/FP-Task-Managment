from django.urls import path

from .views import Authentication, LoginView, TeamAndTaskAPIView, CommentView

urlpatterns = [
    path('create/', Authentication.as_view({'post': 'create_user'}), name='create_user'),
    path('login/', LoginView.as_view({'post': 'login'}), name='login'),
    path('task/add/', TeamAndTaskAPIView.as_view({'post': 'add_tasks'}), name='add_task'),
    path('auth_me/', LoginView.as_view({'post': 'auth_me'}), name='auth_me'),
    path('team/', TeamAndTaskAPIView.as_view({'post': 'team_create'}), name='team'),
    path('task/', TeamAndTaskAPIView.as_view({'post': 'task_create'}), name='task'),
    path('team/add/', TeamAndTaskAPIView.as_view({'post': 'add_team'}), name='add_team'),
    path('comment/<int:pk>/', CommentView.as_view({'post': 'write'}), name='write'),
]
