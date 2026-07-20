from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('quizzes', views.QuizViewSet, basename='quiz')
router.register('certificates', views.CertificateViewSet, basename='certificate')

app_name = 'quizzes_api'

urlpatterns = [
    path('', include(router.urls)),
]