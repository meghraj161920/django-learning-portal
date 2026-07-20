from rest_framework.test import APITestCase
from rest_framework import status
from apps.courses.models import Category, Course
from django.contrib.auth import get_user_model

User = get_user_model()

class CourseAPITest(APITestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(username='instructor', password='pass', role='instructor')
        self.category = Category.objects.create(name='Python', slug='python')
        self.course = Course.objects.create(
            title='Python Basics', slug='python-basics', description='Learn Python',
            category=self.category, instructor=self.instructor, status='published'
        )

    def test_list_courses(self):
        response = self.client.get('/api/courses/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_course_detail(self):
        response = self.client.get(f'/api/courses/courses/{self.course.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Python Basics')