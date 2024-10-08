from tkinter.font import names

from django.urls import path
from .views import Authentication, LoginView

urlpatterns = [
    path('create/', Authentication.as_view({'post': 'create_user'}), name='create_user'),
    path('login/', LoginView.as_view({'post': 'login'}), name='login')
]
