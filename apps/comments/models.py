from django.db import models


class Comment(models.Model):
    lesson = models.ForeignKey(
        'lessons.Lesson',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    content = models.TextField()

    upvotes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'comments'

    def __str__(self):
        return f"Comment by {self.author.username} on {self.lesson.title}"


class CommentUpvote(models.Model):

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='upvote_records'
    )

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='comment_upvotes'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['comment', 'user']
        db_table = 'comment_upvotes'