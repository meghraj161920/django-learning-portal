from django.urls import path
from . import views

app_name = 'accounts_api'

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('profile/', views.ProfileAPIView.as_view(), name='api_profile'),
    path('profile/update/', views.ProfileUpdateAPIView.as_view(), name='api_profile_update'),
    path('users/', views.UserListAPIView.as_view(), name='api_user_list'),
    path('users/<str:username>/', views.PublicProfileAPIView.as_view(), name='api_public_profile'),
]