"""Main URL routing for the blog project."""

from django.urls import path, include
from apps.blog.views import health_check

urlpatterns = [
    # API routes
    path('api/', include('apps.blog.urls')),
    
    # Root health check
    path('', health_check, name='root'),
]
