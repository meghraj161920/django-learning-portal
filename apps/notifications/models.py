from django.db import models


class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ('enrollment', 'Enrollment'),
        ('completion', 'Completion'),
        ('comment', 'Comment'),
        ('reply', 'Reply'),
        ('certificate', 'Certificate'),
    ]

    recipient = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    link = models.URLField(blank=True)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'notifications'

    def __str__(self):
        return f"{self.notification_type}: {self.title}"