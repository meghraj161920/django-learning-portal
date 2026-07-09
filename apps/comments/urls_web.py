from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path(
        '<int:lesson_id>/add/',
        views.AddCommentView.as_view(),
        name='add'
    ),

    path(
        '<int:comment_id>/reply/',
        views.ReplyCommentView.as_view(),
        name='reply'
    ),

    path(
        '<int:comment_id>/upvote/',
        views.UpvoteCommentView.as_view(),
        name='upvote'
    ),
]