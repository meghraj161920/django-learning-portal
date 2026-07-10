from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('course/<slug:course>/<slug:lesson>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]