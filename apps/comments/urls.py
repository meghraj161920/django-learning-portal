from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(
    'comments',
    views.CommentViewSet,
    basename='comment'
)

app_name = 'comments_api'

urlpatterns = [
    path('', include(router.urls)),
]