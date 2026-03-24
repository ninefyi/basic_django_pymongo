"""URL routing for the blog app."""

from django.urls import path
from . import views

urlpatterns = [
    # Health check endpoint
    path('health/', views.health_check, name='health_check'),
    
    # CRUD endpoints
    path('posts/', views.list_posts, name='list_posts'),      # GET all posts, POST new post
    path('posts/<str:post_id>/', views.get_post, name='get_post'),  # GET, PUT, DELETE single post
]
