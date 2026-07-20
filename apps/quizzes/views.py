from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from .models import Quiz, Question, Choice, QuizAttempt, Certificate
from .serializers import (QuizListSerializer, QuizDetailSerializer, QuizSubmitSerializer,
                          QuizResultSerializer, CertificateSerializer)

class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.filter(is_published=True)
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuizDetailSerializer
        return QuizListSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def submit(self, request, slug=None):
        quiz = self.get_object()
        serializer = QuizSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answers = serializer.validated_data['answers']

        score = 0
        total_points = 0
        for question in quiz.questions.all():
            total_points += question.points
            selected_choice_id = answers.get(str(question.id))
            if selected_choice_id:
                correct_choice = question.choices.filter(is_correct=True).first()
                if correct_choice and correct_choice.id == selected_choice_id:
                    score += question.points

        percentage = (score / total_points * 100) if total_points > 0 else 0
        passed = percentage >= quiz.passing_score

        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=score,
            total_points=total_points,
            percentage=round(percentage, 2),
            passed=passed,
            answers=answers
        )

        if passed:
            cert_id = f"CERT-{uuid.uuid4().hex[:8].upper()}"
            Certificate.objects.create(
                student=request.user,
                course=quiz.course,
                quiz_attempt=attempt,
                certificate_id=cert_id
            )

        return Response(QuizResultSerializer(attempt).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def result(self, request, slug=None):
        quiz = self.get_object()
        attempt = QuizAttempt.objects.filter(student=request.user, quiz=quiz).order_by('-started_at').first()
        if not attempt:
            return Response({'error': 'No attempt found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(QuizResultSerializer(attempt).data)

class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'certificate_id'

    def get_queryset(self):
        return Certificate.objects.filter(student=self.request.user)

class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'quizzes/quiz_detail.html'
    slug_url_kwarg = 'quiz_id'
    context_object_name = 'quiz'

    def get_queryset(self):
        return Quiz.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.object.questions.prefetch_related('choices').all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        quiz = self.object
        score = 0
        total_points = 0
        answers = {}
        for question in quiz.questions.all():
            total_points += question.points
            choice_id = request.POST.get(f'question_{question.id}')
            answers[str(question.id)] = choice_id
            if choice_id:
                correct = question.choices.filter(is_correct=True).first()
                if correct and str(correct.id) == choice_id:
                    score += question.points

        percentage = (score / total_points * 100) if total_points > 0 else 0
        passed = percentage >= quiz.passing_score

        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=score,
            total_points=total_points,
            percentage=round(percentage, 2),
            passed=passed,
            answers=answers
        )

        if passed:
            cert_id = f"CERT-{uuid.uuid4().hex[:8].upper()}"
            Certificate.objects.create(
                student=request.user,
                course=quiz.course,
                quiz_attempt=attempt,
                certificate_id=cert_id
            )

        return redirect('quizzes:quiz_result', attempt_id=attempt.id)

class QuizResultView(LoginRequiredMixin, DetailView):
    model = QuizAttempt
    template_name = 'quizzes/quiz_result.html'
    pk_url_kwarg = 'attempt_id'
    context_object_name = 'attempt'

    def get_queryset(self):
        return QuizAttempt.objects.filter(student=self.request.user)

class CertificateView(LoginRequiredMixin, TemplateView):
    template_name = 'quizzes/certificate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cert = get_object_or_404(Certificate, certificate_id=self.kwargs.get('cert_id'), student=self.request.user)
        context['certificate'] = cert
        return context