"""Main URL routing for the blog project."""

from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from apps.blog.views import health_check, crud_ui

urlpatterns = [
    # CRUD UI at root
    path('', crud_ui, name='home'),
    
    # Django admin
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/', include('apps.blog.urls')),
    
    # Health check at /health/
    path('health/', health_check, name='health'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
