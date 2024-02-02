from django.urls import path
from .views import *

urlpatterns = [
    path('sign-up',CustomUserSignup.as_view(),name='sign-up'),
    path('',CustomUserLogin.as_view(),name='login'),
    path('logout/',CustomLogoutView.as_view(),name='logout'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('update/profile/', UpdateProfileView.as_view(),name='update'),
    path('delete/',DeleteProfileView.as_view(),name='delete'),
]