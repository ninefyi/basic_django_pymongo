"""Main URL routing for the blog project."""

from django.urls import path, include
from apps.blog.views import health_check, crud_ui

urlpatterns = [
    # CRUD UI at root
    path('', crud_ui, name='home'),
    
    # API routes
    path('api/', include('apps.blog.urls')),
    
    # Health check at /health/
    path('health/', health_check, name='health'),
]
