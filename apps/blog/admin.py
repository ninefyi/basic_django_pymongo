"""Admin registration for Blog models."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Post, User


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('author',)
    search_fields = ('title', 'content', 'author')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(User, UserAdmin)
