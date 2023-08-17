from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (UserLoginView, LogoutView, UserCreateView, VideoDetailView,
                     VideoListView, VideoStreamView, VideoDetailAPI, VideoListAPI)
from . import views


urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('videos/', views.video_list, name='video-list'),  # HTML view
    path('api/videos/', views.VideoDetailView.as_view(), name='api-video-list'),  # API view
    path('videos/create/', views.video_create, name='video-create'),
    path('videos/<int:pk>/edit/', views.video_edit, name='video-edit'),
    path('videos/<int:pk>/delete/', views.video_delete, name='video-delete'),
    path('search/', views.video_search, name='video-search'),
    path('videos/<int:pk>/', views.video_detail, name='video-detail'),
    path('api/videos/<int:pk>/', views.VideoDetailView.as_view(), name='api-video-detail'),
    path('videos/<int:video_id>/stream/', VideoStreamView.as_view(), name='video-stream'),
    path('api/videos/', VideoListAPI.as_view(), name='api-video-list'),
    path('api/videos/<int:pk>/', VideoDetailAPI.as_view(), name='api-video-detail'),

    path('api/docs/', views.api_documentation, name='api-documentation'),
    # Add other app-specific URLs here
]
