"""Blog models for MongoDB using Django ORM with django-mongodb-backend."""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django_mongodb_backend.fields import ObjectIdAutoField


class Post(models.Model):
    """
    Blog Post model for MongoDB.
    
    This model uses Django's ORM with the mongodb backend, allowing you to
    use familiar Django patterns while storing data in MongoDB documents.
    
    Fields:
    - title: The blog post title (required)
    - content: The blog post content (required)
    - author: Name of the author (optional, defaults to "Anonymous")
    - created_at: Timestamp when post was created (auto-set)
    - updated_at: Timestamp when post was last updated (auto-set)
    """
    
    title = models.CharField(
        max_length=200,
        help_text="Title of the blog post"
    )
    content = models.TextField(
        help_text="Content of the blog post"
    )
    author = models.CharField(
        max_length=100,
        default="Anonymous",
        help_text="Author of the blog post"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the post was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the post was last updated"
    )

    class Meta:
        # MongoDB collection name
        db_table = settings.DATABASES['default'].get('COLLECTION_NAME', 'posts')
        # Default ordering by newest first
        ordering = ['-created_at']
        # Index settings for better query performance
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author']),
        ]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        """String representation of the post."""
        return self.title

    def to_dict(self):
        """Convert post to dictionary for JSON response."""
        return {
            'id': str(self.pk),
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class User(AbstractUser):
    """Custom User model that uses ObjectIdAutoField for MongoDB compatibility."""

    id = ObjectIdAutoField(primary_key=True)

    class Meta:
        app_label = 'blog'
