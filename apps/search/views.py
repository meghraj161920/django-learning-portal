from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from django.views.generic import TemplateView

from apps.courses.models import Course
from apps.courses.serializers import CourseListSerializer
from apps.lessons.models import Lesson
from apps.lessons.serializers import LessonMinimalSerializer


class SearchAPIView(generics.GenericAPIView):
    permission_classes = []

    def get(self, request):
        query = request.query_params.get("q", "")

        if not query or len(query) < 2:
            return Response({
                "courses": [],
                "lessons": []
            })

        courses = Course.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(subtitle__icontains=query),
            status="published"
        )[:10]

        lessons = Lesson.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query),
            status="published"
        ).select_related("course")[:10]

        return Response({
            "courses": CourseListSerializer(courses, many=True).data,
            "lessons": LessonMinimalSerializer(lessons, many=True).data,
            "query": query
        })


class SearchView(TemplateView):
    template_name = "search/search_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get("q", "")

        if query and len(query) >= 2:

            context["courses"] = Course.objects.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(subtitle__icontains=query),
                status="published"
            )[:10]

            context["lessons"] = Lesson.objects.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query),
                status="published"
            ).select_related("course")[:10]

        context["query"] = query

        return context