from django.urls import path
from .views import RegisterView, profileView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/',profileView.as_view(), name='profile'),
]
