from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Comment, CommentUpvote
from .serializers import CommentSerializer, CommentCreateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter(parent=None).select_related(
            'author',
            'lesson'
        )

        lesson_id = self.request.query_params.get('lesson')

        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)

        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateSerializer
        return CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def upvote(self, request, pk=None):

        comment = self.get_object()

        upvote, created = CommentUpvote.objects.get_or_create(
            comment=comment,
            user=request.user
        )

        if not created:
            upvote.delete()
            comment.upvotes = max(0, comment.upvotes - 1)
            comment.save()

            return Response({
                'status': 'upvote removed',
                'upvotes': comment.upvotes
            })

        comment.upvotes += 1
        comment.save()

        return Response({
            'status': 'upvoted',
            'upvotes': comment.upvotes
        })

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reply(self, request, pk=None):

        parent = self.get_object()

        serializer = CommentCreateSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)

        serializer.save(
            parent=parent,
            lesson=parent.lesson
        )

        return Response(
            CommentSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED
        )


class AddCommentView(LoginRequiredMixin, View):

    def post(self, request, lesson_id):

        from apps.lessons.models import Lesson

        lesson = get_object_or_404(Lesson, pk=lesson_id)

        content = request.POST.get("content")

        if content:
            Comment.objects.create(
                lesson=lesson,
                author=request.user,
                content=content
            )

        return redirect(
            "lessons:lesson_detail",
            course=lesson.course.slug,
            lesson=lesson.slug
        )


class ReplyCommentView(LoginRequiredMixin, View):

    def post(self, request, comment_id):

        parent = get_object_or_404(Comment, pk=comment_id)

        content = request.POST.get("content")

        if content:
            Comment.objects.create(
                lesson=parent.lesson,
                author=request.user,
                parent=parent,
                content=content
            )

        return redirect(
            "lessons:lesson_detail",
            course=parent.lesson.course.slug,
            lesson=parent.lesson.slug
        )


class UpvoteCommentView(LoginRequiredMixin, View):

    def post(self, request, comment_id):

        comment = get_object_or_404(Comment, pk=comment_id)

        upvote, created = CommentUpvote.objects.get_or_create(
            comment=comment,
            user=request.user
        )

        if not created:
            upvote.delete()
            comment.upvotes = max(0, comment.upvotes - 1)
        else:
            comment.upvotes += 1

        comment.save()

        return redirect(request.META.get("HTTP_REFERER", "/"))