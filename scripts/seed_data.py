import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User
from apps.courses.models import Category, Course, Tag
from apps.lessons.models import Lesson
from apps.quizzes.models import Quiz, Question, Choice

# Create users
admin, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'role': 'admin', 'is_staff': True, 'is_superuser': True})
admin.set_password('admin123')
admin.save()

instructor, _ = User.objects.get_or_create(username='instructor', defaults={'email': 'instructor@example.com', 'role': 'instructor'})
instructor.set_password('instructor123')
instructor.save()

student, _ = User.objects.get_or_create(username='student', defaults={'email': 'student@example.com', 'role': 'student'})
student.set_password('student123')
student.save()

# Categories
categories = [
    {'name': 'Python', 'slug': 'python', 'description': 'Python programming', 'color': '#3776AB'},
    {'name': 'Django', 'slug': 'django', 'description': 'Django web framework', 'color': '#092E20'},
    {'name': 'JavaScript', 'slug': 'javascript', 'description': 'JavaScript programming', 'color': '#F7DF1E'},
    {'name': 'HTML & CSS', 'slug': 'html-css', 'description': 'Web markup and styling', 'color': '#E34F26'},
    {'name': 'Database', 'slug': 'database', 'description': 'Database design and SQL', 'color': '#4479A1'},
]
for cat_data in categories:
    Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)

# Course
python_cat = Category.objects.get(slug='python')
course, _ = Course.objects.get_or_create(
    slug='python-fundamentals',
    defaults={
        'title': 'Python Fundamentals',
        'subtitle': 'Learn Python from scratch',
        'description': 'A comprehensive course covering Python basics including variables, data types, control flow, functions, and object-oriented programming.',
        'category': python_cat,
        'instructor': instructor,
        'difficulty': 'beginner',
        'status': 'published',
        'estimated_duration': 20,
        'is_featured': True,
    }
)

# Lessons
lessons_data = [
    {
        'title': 'Introduction to Python',
        'slug': 'introduction',
        'content': '# Introduction to Python\n\nPython is a high-level programming language.\n\n## Why Python?\n\n- Easy to learn\n- Large community\n- Versatile\n\n```python\nprint("Hello, World!")\n```',
        'order': 1,
        'duration_minutes': 15,
        'is_free': True,
    },
    {
        'title': 'Variables and Data Types',
        'slug': 'variables-data-types',
        'content': '# Variables and Data Types\n\nIn Python, variables are created when you assign a value.\n\n```python\nname = "Alice"\nage = 25\n```',
        'order': 2,
        'duration_minutes': 20,
    },
    {
        'title': 'Control Flow',
        'slug': 'control-flow',
        'content': '# Control Flow\n\n## If Statements\n\n```python\nage = 18\nif age >= 18:\n    print("You are an adult")\n```',
        'order': 3,
        'duration_minutes': 25,
    },
]

for lesson_data in lessons_data:
    Lesson.objects.get_or_create(course=course, slug=lesson_data['slug'], defaults=lesson_data)

# Quiz
quiz, _ = Quiz.objects.get_or_create(course=course, slug='python-basics-quiz', defaults={'title': 'Python Basics Quiz', 'is_published': True, 'passing_score': 70})
q1, _ = Question.objects.get_or_create(quiz=quiz, order=1, defaults={'text': 'What is the output of print(2 + 2)?', 'points': 10})
Choice.objects.get_or_create(question=q1, text='4', defaults={'is_correct': True})
Choice.objects.get_or_create(question=q1, text='22', defaults={'is_correct': False})

q2, _ = Question.objects.get_or_create(quiz=quiz, order=2, defaults={'text': 'Which keyword defines a function?', 'points': 10})
Choice.objects.get_or_create(question=q2, text='def', defaults={'is_correct': True})
Choice.objects.get_or_create(question=q2, text='function', defaults={'is_correct': False})

print("Seed data created successfully!")
print("Admin: admin / admin123")
print("Instructor: instructor / instructor123")
print("Student: student / student123")
