from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('lessons', views.LessonViewSet, basename='lesson')

app_name = 'lessons_api'

urlpatterns = [
    path('', include(router.urls)),
]