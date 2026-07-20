from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from django.views.generic import ListView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        )

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()

        return Response({
            'status': 'marked as read'
        })

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().filter(
            is_read=False
        ).update(is_read=True)

        return Response({
            'status': 'all marked as read'
        })

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = self.get_queryset().filter(
            is_read=False
        ).count()

        return Response({
            'unread_count': count
        })


class NotificationListView(LoginRequiredMixin, ListView):
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        )


class MarkReadView(LoginRequiredMixin, View):

    def post(self, request, pk):

        notification = get_object_or_404(
            Notification,
            pk=pk,
            recipient=request.user
        )

        notification.is_read = True
        notification.save()

        return redirect('notifications:notification_list')


class MarkAllReadView(LoginRequiredMixin, View):

    def post(self, request):

        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)

        return redirect('notifications:notification_list')