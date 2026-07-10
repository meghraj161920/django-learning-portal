from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('courses', views.CourseViewSet, basename='course')
router.register('tags', views.TagViewSet, basename='tag')

app_name = 'courses_api'

urlpatterns = [
    path('', include(router.urls)),
]