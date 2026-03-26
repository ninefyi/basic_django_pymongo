"""Django management command to seed the database with sample blog posts."""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.blog.models import Post


class Command(BaseCommand):
    help = "Populate MongoDB with sample blog posts"

    def handle(self, *args, **options):
        Post.objects.all().delete()
        self.stdout.write("Cleared existing posts")

        sample_posts = [
            {
                "title": "Welcome to Django + MongoDB",
                "content": "This is the first blog post in our workshop. Django and MongoDB work together beautifully to create flexible, scalable web applications.",
                "author": "Alice",
            },
            {
                "title": "Understanding MongoDB Collections",
                "content": "MongoDB stores data in collections of documents. Each document is like a JSON object, making it very flexible compared to traditional SQL databases.",
                "author": "Bob",
            },
            {
                "title": "REST APIs Explained",
                "content": "REST (Representational State Transfer) is a way to design web APIs. CRUD operations map nicely to HTTP methods: POST (Create), GET (Read), PUT (Update), DELETE (Delete).",
                "author": "Alice",
            },
            {
                "title": "Getting Started with Django",
                "content": 'Django is a powerful Python web framework that makes building web applications fast and easy. It follows the "batteries included" philosophy, providing most tools you need out of the box.',
                "author": "Charlie",
            },
            {
                "title": "Best Practices for API Design",
                "content": "When designing APIs, think about your users. Make URLs intuitive, use consistent naming, provide clear error messages, and document everything well.",
                "author": "David",
            },
        ]

        for i, post_data in enumerate(sample_posts):
            Post.objects.create(
                title=post_data["title"],
                content=post_data["content"],
                author=post_data["author"],
                created_at=timezone.now() - timedelta(days=len(sample_posts) - i),
            )
            self.stdout.write(
                self.style.SUCCESS(f"✓ Created: '{post_data['title']}' by {post_data['author']}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"\nSuccessfully created {len(sample_posts)} sample posts!")
        )
