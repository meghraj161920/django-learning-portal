from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Lesson
from .serializers import LessonSerializer, LessonCreateUpdateSerializer, LessonMinimalSerializer
from apps.courses.permissions import IsInstructorOrReadOnly

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(status='published')
    lookup_field = 'slug'
    permission_classes = [IsInstructorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LessonCreateUpdateSerializer
        return LessonSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if course_slug := self.request.query_params.get('course'):
            queryset = queryset.filter(course__slug=course_slug)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def complete(self, request, slug=None):
        lesson = self.get_object()
        from apps.progress.models import LessonProgress
        progress, created = LessonProgress.objects.get_or_create(
            student=request.user, lesson=lesson,
            defaults={'is_completed': True}
        )
        if not created:
            progress.is_completed = True
            progress.save()
        return Response({'status': 'completed'})

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    context_object_name = 'lesson'

    def get_object(self, queryset=None):
        course_slug = self.kwargs.get('course')
        lesson_slug = self.kwargs.get('lesson')
        return get_object_or_404(Lesson, course__slug=course_slug, slug=lesson_slug, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.object
        context['course'] = lesson.course
        context['toc'] = lesson.extract_toc()
        context['next_lesson'] = lesson.get_next_lesson()
        context['prev_lesson'] = lesson.get_prev_lesson()
        context['all_lessons'] = lesson.course.lessons.filter(status='published').order_by('order')
        return context