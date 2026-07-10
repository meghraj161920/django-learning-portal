from rest_framework import serializers
from .models import Lesson
from apps.courses.serializers import CourseListSerializer

class LessonMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'slug', 'order', 'duration_minutes', 'is_free']

class LessonSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    toc = serializers.SerializerMethodField()
    next_lesson = serializers.SerializerMethodField()
    prev_lesson = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'slug', 'content', 'content_html', 'course',
                  'order', 'duration_minutes', 'is_free', 'video_url', 'status',
                  'toc', 'next_lesson', 'prev_lesson', 'is_completed', 'created_at']
        read_only_fields = ['content_html', 'toc']

    def get_toc(self, obj):
        return obj.extract_toc()

    def get_next_lesson(self, obj):
        next_l = obj.get_next_lesson()
        if next_l:
            return {'title': next_l.title, 'slug': next_l.slug}
        return None

    def get_prev_lesson(self, obj):
        prev_l = obj.get_prev_lesson()
        if prev_l:
            return {'title': prev_l.title, 'slug': prev_l.slug}
        return None

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.progress.models import LessonProgress
            return LessonProgress.objects.filter(student=request.user, lesson=obj, is_completed=True).exists()
        return False

class LessonCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'slug', 'content', 'order', 'duration_minutes', 'is_free', 'video_url', 'status']