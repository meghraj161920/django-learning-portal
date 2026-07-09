from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(
    'notifications',
    views.NotificationViewSet,
    basename='notification'
)

app_name = 'notifications_api'

urlpatterns = [
    path('', include(router.urls)),
]