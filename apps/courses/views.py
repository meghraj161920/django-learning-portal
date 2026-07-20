from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import ListView, DetailView, TemplateView
from .models import Category, Course, Tag
from .serializers import CategorySerializer, CourseListSerializer, CourseDetailSerializer, TagSerializer
from .permissions import IsInstructorOrReadOnly

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(status='published')
    serializer_class = CourseListSerializer
    lookup_field = 'slug'
    permission_classes = [IsInstructorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'is_featured']
    search_fields = ['title', 'subtitle', 'description']
    ordering_fields = ['created_at', 'estimated_duration', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, slug=None):
        course = self.get_object()
        from apps.progress.models import Enrollment
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user, course=course
        )
        if created:
            return Response({'status': 'enrolled'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already enrolled'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unenroll(self, request, slug=None):
        course = self.get_object()
        from apps.progress.models import Enrollment
        Enrollment.objects.filter(student=request.user, course=course).delete()
        return Response({'status': 'unenrolled'}, status=status.HTTP_200_OK)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'

class HomeView(TemplateView):
    template_name = 'courses/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_courses'] = Course.objects.filter(is_featured=True, status='published')[:6]
        context['latest_courses'] = Course.objects.filter(status='published')[:8]
        context['categories'] = Category.objects.all()
        return context

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12

    def get_queryset(self):
        queryset = Course.objects.filter(status='published')
        if category := self.request.GET.get('category'):
            queryset = queryset.filter(category__slug=category)
        if difficulty := self.request.GET.get('difficulty'):
            queryset = queryset.filter(difficulty=difficulty)
        if search := self.request.GET.get('search'):
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['difficulties'] = Course.DIFFICULTY_CHOICES
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'course'

    def get_queryset(self):
        return Course.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            from apps.progress.models import Enrollment
            context['is_enrolled'] = Enrollment.objects.filter(
                student=self.request.user, course=self.object
            ).exists()
<<<<<<< HEAD
        return context
=======
        return context


from rest_framework import permissions

class IsInstructorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_instructor

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.instructor == request.user
>>>>>>> origin/release/day-10
