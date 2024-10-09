from django.urls import path

from .views import Authentication, LoginView, TeamAndTaskAPIView

urlpatterns = [
    path('create/', Authentication.as_view({'post': 'create_user'}), name='create_user'),
    path('login/', LoginView.as_view({'post': 'login'}), name='login'),
    path('auth_me/', LoginView.as_view({'post': 'auth_me'}), name='auth_me'),
    path('team/', TeamAndTaskAPIView.as_view({'post': 'create'}), name='team'),
]
