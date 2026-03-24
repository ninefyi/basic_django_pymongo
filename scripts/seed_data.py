"""
Script to populate MongoDB with sample blog posts.
Run this to create demo data for testing.

Usage:
    python seed_data.py
"""

import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blog.models import Post
from datetime import datetime, timedelta
from django.utils import timezone


def create_sample_posts():
    """Create sample blog posts in MongoDB."""
    
    # Clear existing posts
    Post.objects.delete()
    print("Cleared existing posts")
    
    # Create sample posts with different authors and dates
    sample_posts = [
        {
            'title': 'Welcome to Django + MongoDB',
            'content': 'This is the first blog post in our workshop. Django and MongoDB work together beautifully to create flexible, scalable web applications.',
            'author': 'Alice'
        },
        {
            'title': 'Understanding MongoDB Collections',
            'content': 'MongoDB stores data in collections of documents. Each document is like a JSON object, making it very flexible compared to traditional SQL databases.',
            'author': 'Bob'
        },
        {
            'title': 'REST APIs Explained',
            'content': 'REST (Representational State Transfer) is a way to design web APIs. CRUD operations map nicely to HTTP methods: POST (Create), GET (Read), PUT (Update), DELETE (Delete).',
            'author': 'Alice'
        },
        {
            'title': 'Getting Started with Django',
            'content': 'Django is a powerful Python web framework that makes building web applications fast and easy. It follows the "batteries included" philosophy, providing most tools you need out of the box.',
            'author': 'Charlie'
        },
        {
            'title': 'Best Practices for API Design',
            'content': 'When designing APIs, think about your users. Make URLs intuitive, use consistent naming, provide clear error messages, and document everything well.',
            'author': 'David'
        },
    ]
    
    # Create and save posts
    for i, post_data in enumerate(sample_posts):
        post = Post(
            title=post_data['title'],
            content=post_data['content'],
            author=post_data['author'],
            created_at=timezone.now() - timedelta(days=len(sample_posts) - i)
        )
        post.save()
        print(f"✓ Created post: '{post.title}' by {post.author}")
    
    print(f"\nSuccessfully created {len(sample_posts)} sample posts!")
    print("\nTo verify, run:")
    print("  python manage.py shell")
    print("  >>> from blog.models import Post")
    print("  >>> Post.objects.count()")


if __name__ == '__main__':
    try:
        create_sample_posts()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure MongoDB is running before running this script!")
