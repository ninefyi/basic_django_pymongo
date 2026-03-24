"""Blog views for CRUD operations using Django ORM."""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
import json

from .models import Post


@require_http_methods(["POST"])
def create_post(request):
    """
    CREATE: Add a new blog post to MongoDB.
    
    Expected JSON body:
    {
        "title": "My First Post",
        "content": "Hello world...",
        "author": "Alice"  (optional, defaults to "Anonymous")
    }
    
    Returns: JSON with post ID and status
    """
    try:
        # Parse JSON from request body
        data = json.loads(request.body)
        
        # Validate required fields
        if 'title' not in data or 'content' not in data:
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields: title and content'
            }, status=400)
        
        # Create new post with provided data
        post = Post.objects.create(
            title=data.get('title'),
            content=data.get('content'),
            author=data.get('author', 'Anonymous')
        )
        
        # Return success response with the new post's ID
        return JsonResponse({
            'status': 'success',
            'message': 'Post created successfully',
            'post': post.to_dict()
        }, status=201)
        
    except ValueError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON in request body'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error creating post: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def list_posts(request):
    """
    READ: Get all blog posts from MongoDB.
    
    Query parameters:
    - author: Filter by author name (optional)
    - limit: Number of posts to return (optional, default: 50)
    
    Returns: JSON list of all posts
    """
    try:
        # Get query parameters
        author = request.GET.get('author')
        try:
            limit = int(request.GET.get('limit', 50))
        except ValueError:
            limit = 50
        
        # Build query using Django ORM
        if author:
            posts = Post.objects.filter(author=author)[:limit]
        else:
            posts = Post.objects.all()[:limit]
        
        # Convert posts to list of dictionaries
        posts_list = [post.to_dict() for post in posts]
        
        return JsonResponse({
            'status': 'success',
            'count': len(posts_list),
            'posts': posts_list
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error fetching posts: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def get_post(request, post_id):
    """
    READ: Get a single blog post by ID.
    
    URL parameter:
    - post_id: MongoDB ObjectId or Django primary key of the post
    
    Returns: JSON with the post details
    """
    try:
        # Try to find post by ID
        try:
            # Try converting to int first (if MongoDB backend uses numeric IDs)
            post_id_converted = int(post_id)
            post = Post.objects.get(pk=post_id_converted)
        except (ValueError, ObjectDoesNotExist):
            # If not a number or not found, try as string (ObjectId)
            post = Post.objects.get(pk=post_id)
        
        return JsonResponse({
            'status': 'success',
            'post': post.to_dict()
        }, status=200)
        
    except ObjectDoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Post not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error fetching post: {str(e)}'
        }, status=500)


@require_http_methods(["PUT"])
def update_post(request, post_id):
    """
    UPDATE: Modify an existing blog post.
    
    URL parameter:
    - post_id: MongoDB ObjectId or Django primary key of the post
    
    Expected JSON body (all fields optional):
    {
        "title": "Updated Title",
        "content": "Updated content...",
        "author": "New Author"
    }
    
    Returns: JSON with updated post details
    """
    try:
        # Parse JSON from request body
        data = json.loads(request.body)
        
        # Try to find post by ID
        try:
            post_id_converted = int(post_id)
            post = Post.objects.get(pk=post_id_converted)
        except (ValueError, ObjectDoesNotExist):
            post = Post.objects.get(pk=post_id)
        
        # Update fields if provided
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
        if 'author' in data:
            post.author = data['author']
        
        # Save to MongoDB (updated_at is auto-updated via auto_now=True)
        post.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Post updated successfully',
            'post': post.to_dict()
        }, status=200)
        
    except ValueError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON in request body'
        }, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Post not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error updating post: {str(e)}'
        }, status=500)


@require_http_methods(["DELETE"])
def delete_post(request, post_id):
    """
    DELETE: Remove a blog post from MongoDB.
    
    URL parameter:
    - post_id: MongoDB ObjectId or Django primary key of the post
    
    Returns: JSON confirmation of deletion
    """
    try:
        # Try to find and delete post by ID
        try:
            post_id_converted = int(post_id)
            post = Post.objects.get(pk=post_id_converted)
        except (ValueError, ObjectDoesNotExist):
            post = Post.objects.get(pk=post_id)
        
        post.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Post deleted successfully'
        }, status=200)
        
    except ObjectDoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Post not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error deleting post: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint to verify the API is running."""
    return JsonResponse({
        'status': 'success',
        'message': 'Blog API is running!'
    })

