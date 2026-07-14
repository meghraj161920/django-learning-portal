from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import User
from .forms import UserRegistrationForm
from .serializers import (UserSerializer, UserRegistrationSerializer, 
                          ProfileUpdateSerializer, PublicProfileSerializer)

# API Views
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class PublicProfileAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = PublicProfileSerializer
    lookup_field = 'username'
    permission_classes = [permissions.AllowAny]

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.AllowAny]

# Web Views
class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

class LoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class LogoutView(BaseLogoutView):
    next_page = '/'
    http_method_names = ['get', 'post']

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'

    def get_object(self):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'bio', 'avatar', 'github_url', 'linkedin_url']
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

class PublicProfileView(DetailView):
    model = User
    template_name = 'accounts/public_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile_user'

# Create your views here.
