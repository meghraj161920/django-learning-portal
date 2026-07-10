from rest_framework import serializers
from .models import Category, Course, Tag
from apps.accounts.serializers import PublicProfileSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    course_count = serializers.IntegerField(source='courses.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'color', 'icon', 'course_count']

class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    instructor = PublicProfileSerializer(read_only=True)
    lesson_count = serializers.IntegerField(read_only=True)
    enrolled_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'subtitle', 'slug', 'thumbnail', 'difficulty', 
                  'category', 'instructor', 'estimated_duration', 'is_featured',
                  'lesson_count', 'enrolled_count', 'created_at']

class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    instructor = PublicProfileSerializer(read_only=True)
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'subtitle', 'slug', 'description', 'category',
                  'tags', 'instructor', 'difficulty', 'status', 'thumbnail',
                  'estimated_duration', 'is_featured', 'lessons', 'created_at', 'updated_at']

    def get_lessons(self, obj):
        from apps.lessons.serializers import LessonMinimalSerializer
        lessons = obj.lessons.filter(status='published').order_by('order')
        return LessonMinimalSerializer(lessons, many=True, read_only=True).data