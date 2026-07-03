from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    email_verified = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    @property
    def is_instructor(self):
        return self.role == 'instructor'

    @property
    def is_student(self):
        return self.role == 'student'