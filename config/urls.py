from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # App APIs
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/lessons/', include('apps.lessons.urls')),
    path('api/progress/', include('apps.progress.urls')),
    path('api/bookmarks/', include('apps.bookmarks.urls')),
    path('api/quizzes/', include('apps.quizzes.urls')),
    path('api/search/', include('apps.search.urls')),
    path('api/comments/', include('apps.comments.urls')),
    path('api/notifications/', include('apps.notifications.urls')),

    # Web Views (Templates)
    path('', include('apps.courses.urls_web')),
    path('accounts/', include('apps.accounts.urls_web')),
    # path('courses/', include('apps.courses.urls_web')),
    path('lessons/', include('apps.lessons.urls_web')),
    path('progress/', include('apps.progress.urls_web')),
    path('bookmarks/', include('apps.bookmarks.urls_web')),
    path('quizzes/', include('apps.quizzes.urls_web')),
    path('search/', include('apps.search.urls_web')),
    path('comments/', include('apps.comments.urls_web')),
    path('notifications/', include('apps.notifications.urls_web')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)