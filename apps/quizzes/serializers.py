from rest_framework import serializers
from .models import Quiz, Question, Choice, QuizAttempt, Certificate

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'order', 'points', 'choices']

class QuizListSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(source='questions.count', read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'slug', 'description', 'passing_score', 
                  'time_limit_minutes', 'question_count', 'is_published']

class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'slug', 'description', 'passing_score', 
                  'time_limit_minutes', 'questions', 'is_published']

class QuizSubmitSerializer(serializers.Serializer):
    answers = serializers.DictField(child=serializers.IntegerField())

class QuizResultSerializer(serializers.ModelSerializer):
    quiz = QuizListSerializer(read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'score', 'total_points', 'percentage', 
                  'passed', 'started_at', 'completed_at']

class CertificateSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)

    class Meta:
        model = Certificate
        fields = ['id', 'certificate_id', 'course_title', 'student_name', 'issued_at']