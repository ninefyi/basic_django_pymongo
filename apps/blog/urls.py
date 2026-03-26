"""URL routing for the blog app."""

from django.urls import path
from . import views

urlpatterns = [
    # UI endpoint
    path('', views.crud_ui, name='crud_ui'),
    
    # Health check endpoint
    path('health/', views.health_check, name='health_check'),
    
    # CRUD API endpoints
    path('posts/', views.list_posts, name='list_posts'),
    path('posts/<str:post_id>/', views.get_post, name='get_post'),
]
