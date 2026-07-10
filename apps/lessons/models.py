from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import markdown
from bs4 import BeautifulSoup

class Lesson(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField(help_text='Write in Markdown')
    content_html = models.TextField(blank=True, editable=False)
    order = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=15)
    is_free = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    video_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['course', 'slug']
        db_table = 'lessons'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.content_html = markdown.markdown(
            self.content,
            extensions=['extra', 'codehilite', 'toc', 'tables', 'fenced_code']
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def get_next_lesson(self):
        return self.course.lessons.filter(order__gt=self.order, status='published').first()

    def get_prev_lesson(self):
        return self.course.lessons.filter(order__lt=self.order, status='published').last()

    def extract_toc(self):
        soup = BeautifulSoup(self.content_html, 'html.parser')
        toc = []
        for heading in soup.find_all(['h2', 'h3']):
            toc.append({
                'level': int(heading.name[1]),
                'text': heading.get_text(),
                'id': heading.get('id', slugify(heading.get_text()))
            })
            if not heading.get('id'):
                heading['id'] = slugify(heading.get_text())
        return toc