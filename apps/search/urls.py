from django.urls import path
from . import views

app_name = "search_api"

urlpatterns = [
    path("", views.SearchAPIView.as_view(), name="api_search"),
]