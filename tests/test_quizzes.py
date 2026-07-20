from rest_framework.test import APITestCase
from rest_framework import status
from apps.quizzes.models import Quiz, Question, Choice
from apps.courses.models import Course, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class QuizAPITest(APITestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='student', password='pass')
        self.instructor = User.objects.create_user(username='instructor', password='pass', role='instructor')
        self.category = Category.objects.create(name='Test', slug='test')
        self.course = Course.objects.create(title='Test', slug='test', category=self.category, instructor=self.instructor, status='published')
        self.quiz = Quiz.objects.create(course=self.course, title='Quiz 1', slug='quiz-1', is_published=True)
        self.q1 = Question.objects.create(quiz=self.quiz, text='Q1', order=1, points=10)
        self.c1 = Choice.objects.create(question=self.q1, text='Correct', is_correct=True)
        self.c2 = Choice.objects.create(question=self.q1, text='Wrong', is_correct=False)

    def test_submit_quiz(self):
        self.client.force_authenticate(user=self.student)
        data = {'answers': {str(self.q1.id): self.c1.id}}
        response = self.client.post(f'/api/quizzes/quizzes/{self.quiz.slug}/submit/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['percentage'], 100.0)
        self.assertTrue(response.data['passed'])