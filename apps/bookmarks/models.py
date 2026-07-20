from django.db import models
from django.conf import settings
from apps.courses.models import Course


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"