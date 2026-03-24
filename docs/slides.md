# Django + MongoDB CRUD Workshop

## A Beginner's Guide to Building Web Applications

---

## 📍 Section 1: What is Django & MongoDB?

**⏱️ Time: 5 minutes**

### What is Django?

- **Web Framework** — A collection of tools that help you build websites quickly
- **Like a Toolbox** — Instead of building from scratch, Django provides ready-made pieces
- **Python-based** — Written in Python, easy to learn and read

### What is MongoDB?

- **NoSQL Database** — Stores data differently than traditional databases
- **Document-based** — Saves data as JSON-like documents (flexible structure)
- **Scalable** — Grows easily as your data grows

### Why Django + MongoDB?

| Feature | Benefit |
|---------|---------|
| **Rapid Development** | Build websites in days, not months |
| **Flexible Schema** | Change your data structure anytime |
| **Easy to Learn** | Perfect for beginners and non-technical users |
| **Production Ready** | Used by thousands of companies |

### Real-World Analogy

Think of MongoDB as a filing cabinet where each folder (document) can have different papers inside. Django is your assistant who organizes everything and helps you find what you need.

---

## 📍 Section 2: Installation & Setup (Complete Blog Project)

**⏱️ Time: 10 minutes**

### Step 1: Setup Your Environment

**Option A: GitHub Codespace (Easiest - No Installation Needed)**

1. Click "Code" → "Codespaces" → "Create codespace on main"
2. Wait 1-2 minutes for environment to load
3. Skip to "Step 2: Create MongoDB Atlas Connection"

**Option B: Local Machine**

Requirements: Python 3.9+, Git

```bash
# 1. Create project directory
mkdir blog-project
cd blog-project

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Create requirements.txt with dependencies
cat > requirements.txt << 'EOF'
Django
django-mongodb-backend
pymongo
python-dotenv
EOF

# 5. Install dependencies
pip install -r requirements.txt

# Verify installation
python --version
django-admin --version
```

### Step 2: Create MongoDB Atlas Connection

**Get Your Connection String:**

1. Go to <https://www.mongodb.com/cloud/atlas>
2. Create free account
3. Create M0 (free) cluster
4. Click "Connect" → "Connect your application"
5. Copy connection string: `mongodb+srv://username:password@cluster.mongodb.net/...`
6. Create `.env` file in project root:

```bash
# .env file
MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/blog_db?retryWrites=true&w=majority
DJANGO_SECRET_KEY=your-secret-key-here-change-this
DEBUG=True
```

### Step 3: Initialize Django Project

```bash
# Create Django project (professional structure)
django-admin startproject config .

# Create apps directory
mkdir -p apps/blog

# Create Django app inside apps/
python manage.py startapp blog apps/blog

# Create supporting directories
mkdir -p scripts tests docs
```

**Expected Project Structure:**

```
blog-project/
├── config/              (Django configuration)
│   ├── __init__.py
│   ├── settings.py      (configuration file - we'll edit this)
│   ├── urls.py          (main routes - we'll edit this)
│   └── wsgi.py
│
├── apps/
│   └── blog/            (blog application)
│       ├── __init__.py
│       ├── apps.py      (app config)
│       ├── models.py    (database models - we'll edit this)
│       ├── views.py     (API endpoints - we'll edit this)
│       └── urls.py      (blog routes - we'll create this)
│
├── scripts/
│   └── seed_data.py     (sample data loader)
├── tests/
│   └── test_api.py      (API tests)
├── docs/                (workshop documentation)
├── manage.py
├── requirements.txt
└── .env
```

### What Gets Installed?

- **Django** — Web framework
- **django-mongodb-backend** — ORM bridge for MongoDB
- **pymongo** — MongoDB Python driver
- **python-dotenv** — Load environment variables from .env

---

## 📍 Section 3: Building the Blog - Data Model

**⏱️ Time: 5 minutes**

### Understanding CRUD

CRUD is four basic operations for managing data:

| Operation | What It Does | Real-World Example |
|-----------|-------------|-------------------|
| **Create** | Add new data | Write a new blog post |
| **Read** | Get data | View all blog posts |
| **Update** | Change existing data | Edit a blog post |
| **Delete** | Remove data | Remove a blog post |

### Step 1: Create the Post Model

Edit `blog/models.py`:

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, default="Anonymous")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
    
    def __str__(self):
        return self.title
```

**What This Means:**

- `title` — Blog title (max 200 chars)
- `content` — Blog body text (unlimited)
- `author` — Who wrote it (default: "Anonymous")
- `created_at` — Auto-set when created
- `updated_at` — Auto-updates when modified
- `db_table = 'posts'` — MongoDB collection name

### Step 2: Configure Django for MongoDB

Edit `config/settings.py`:

Find the `DATABASES` section and replace it with:

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_backend',
        'CLIENT': {
            'mongoURI': os.getenv('MONGODB_URI', 'mongodb://localhost:27017/blog_db')
        }
    }
}
```

Make sure `INSTALLED_APPS` includes:

```python
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'apps.blog',  # Add this line
]
```

### Step 3: Update Settings for MongoDB

In `config/settings.py`, find and modify:

```python
# Load environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Secret key
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-key-change-in-production')

# Debug mode
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# MongoDB instead of SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_backend',
        'CLIENT': {
            'mongoURI': os.getenv('MONGODB_URI')
        }
    }
}
```

---

## 📍 Section 4: Building API Endpoints - CREATE

**⏱️ Time: 10 minutes**

### Step 1: Create Views (API Endpoints)

Edit `blog/views.py`:

```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from .models import Post
import json

@require_http_methods(["POST"])
def create_post(request):
    """Create a new blog post"""
    try:
        data = json.loads(request.body)
        
        # Create new post using Django ORM
        post = Post.objects.create(
            title=data.get('title'),
            content=data.get('content'),
            author=data.get('author', 'Anonymous')
        )
        
        # Return success message
        return JsonResponse({
            'status': 'success',
            'id': str(post.pk),
            'message': 'Post created successfully'
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_http_methods(["GET"])
def list_posts(request):
    """Get all blog posts"""
    try:
        posts = Post.objects.all()
        
        posts_list = [{
            'id': str(post.pk),
            'title': post.title,
            'content': post.content,
            'author': post.author,
            'created_at': post.created_at.isoformat()
        } for post in posts]
        
        return JsonResponse({
            'status': 'success',
            'count': len(posts_list),
            'posts': posts_list
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_http_methods(["GET"])
def get_post(request, post_id):
    """Get a single blog post"""
    try:
        post = Post.objects.get(pk=post_id)
        
        return JsonResponse({
            'status': 'success',
            'id': str(post.pk),
            'title': post.title,
            'content': post.content,
            'author': post.author,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat()
        })
        
    except ObjectDoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Post not found'
        }, status=404)

@require_http_methods(["PUT"])
def update_post(request, post_id):
    """Update a blog post"""
    try:
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id)
        
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
        if 'author' in data:
            post.author = data['author']
        
        post.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Post updated successfully',
            'id': str(post.pk)
        })
        
    except ObjectDoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Post not found'
        }, status=404)

@require_http_methods(["DELETE"])
def delete_post(request, post_id):
    """Delete a blog post"""
    try:
        post = Post.objects.get(pk=post_id)
        post.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Post deleted successfully'
        })
        
    except ObjectDoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Post not found'
        }, status=404)
```

### Step 2: Create URL Routes

Create `apps/blog/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.list_posts, name='list_posts'),
    path('posts/<str:post_id>/', views.get_post, name='get_post'),
    path('posts/', views.create_post, name='create_post'),
    path('posts/<str:post_id>/', views.update_post, name='update_post'),
    path('posts/<str:post_id>/', views.delete_post, name='delete_post'),
]
```

### Step 3: Add Routes to Main Project

Edit `config/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.blog.urls')),
]
```

### Step 4: Test CREATE Endpoint

Run Django server:

```bash
# Start the server
python manage.py runserver

# Server will start at http://localhost:8000/
```

**Test creating a post (in another terminal):**

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post",
    "content": "Hello World! This is my first blog post.",
    "author": "Alice"
  }'
```

**Expected Response:**

```json
{
  "status": "success",
  "id": "507f1f77bcf86cd799439011",
  "message": "Post created successfully"
}
```

**Copy the ID** - You'll use it for reading, updating, and deleting!

---

## 📍 Section 5: Testing - READ Operations

**⏱️ Time: 10 minutes**

### Understanding the Flow

When you GET from the API:

```
┌─────────────┐        ┌─────────────────┐        ┌──────────┐
│   Client    │   →    │  Django View    │   →    │ MongoDB  │
│   (curl)    │        │  (get_post)     │        │ (posts)  │
└─────────────┘        └─────────────────┘        └──────────┘
```

### Test 1: Read ALL Posts

```bash
curl http://localhost:8000/api/posts/
```

**Expected Output:**

```json
{
  "status": "success",
  "count": 1,
  "posts": [
    {
      "id": "507f1f77bcf86cd799439011",
      "title": "My First Blog Post",
      "content": "Hello World! This is my first blog post.",
      "author": "Alice",
      "created_at": "2024-03-24T10:30:45.123456+00:00"
    }
  ]
}
```

**What This Means:**

- Count: 1 post in the database
- The post we just created!

### Test 2: Read ONE Post (by ID)

Use the ID from CREATE response:

```bash
curl http://localhost:8000/api/posts/507f1f77bcf86cd799439011/
```

**Expected Output:**

```json
{
  "status": "success",
  "id": "507f1f77bcf86cd799439011",
  "title": "My First Blog Post",
  "content": "Hello World! This is my first blog post.",
  "author": "Alice",
  "created_at": "2024-03-24T10:30:45.123456+00:00",
  "updated_at": "2024-03-24T10:30:45.123456+00:00"
}
```

### Try Creating More Posts

```bash
# Post 2
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learning Django",
    "content": "Django makes web development so easy!",
    "author": "Bob"
  }'

# Post 3
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "MongoDB is Flexible",
    "content": "No rigid schemas - perfect for prototyping!",
    "author": "Charlie"
  }'
```

### Now Read All Posts Again

```bash
curl http://localhost:8000/api/posts/
```

**Expected Output:**

```json
{
  "status": "success",
  "count": 3,
  "posts": [
    {
      "id": "507f1f77bcf86cd799439011",
      "title": "My First Blog Post",
      "author": "Alice",
      ...
    },
    {
      "id": "507f1f77bcf86cd799439012",
      "title": "Learning Django",
      "author": "Bob",
      ...
    },
    {
      "id": "507f1f77bcf86cd799439013",
      "title": "MongoDB is Flexible",
      "author": "Charlie",
      ...
    }
  ]
}
```

Now you have 3 blog posts in MongoDB!

---

## 📍 Section 6: Testing - UPDATE & DELETE Operations

**⏱️ Time: 10 minutes**

### Test 1: UPDATE a Post

Use one of the post IDs from your list:

```bash
# Update the first post
curl -X PUT http://localhost:8000/api/posts/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My UPDATED First Blog Post",
    "content": "This post has been edited!"
  }'
```

**Expected Response:**

```json
{
  "status": "success",
  "message": "Post updated successfully",
  "id": "507f1f77bcf86cd799439011"
}
```

**Verify the Update:**

```bash
curl http://localhost:8000/api/posts/507f1f77bcf86cd799439011/
```

**Notice:** The title and content changed, but:

- `created_at` stays the same (when originally created)
- `updated_at` changed to now

### Test 2: DELETE a Post

Delete the second post:

```bash
curl -X DELETE http://localhost:8000/api/posts/507f1f77bcf86cd799439012/
```

**Expected Response:**

```json
{
  "status": "success",
  "message": "Post deleted successfully"
}
```

**Verify the Delete:**

```bash
# Count posts
curl http://localhost:8000/api/posts/
```

**Expected:** Only 2 posts remain (the deleted one is gone!)

**Try Getting the Deleted Post:**

```bash
curl http://localhost:8000/api/posts/507f1f77bcf86cd799439012/
```

**Expected:**

```json
{
  "status": "error",
  "message": "Post not found"
}
```

### Test 3: Try All Operations Together

**Create a test post:**

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Post",
    "content": "Testing CRUD operations",
    "author": "Tester"
  }'
```

**Copy the ID from response, then:**

```bash
# 1. Read it
curl http://localhost:8000/api/posts/[PASTE_ID]/

# 2. Update it
curl -X PUT http://localhost:8000/api/posts/[PASTE_ID]/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Post - Updated"}'

# 3. Read again to verify
curl http://localhost:8000/api/posts/[PASTE_ID]/

# 4. Delete it
curl -X DELETE http://localhost:8000/api/posts/[PASTE_ID]/

# 5. Try reading (should get error)
curl http://localhost:8000/api/posts/[PASTE_ID]/
```

### Complete CRUD Summary Table

| Operation | HTTP Method | Endpoint | Creation |
|-----------|-------------|----------|----------|
| **Create** | POST | `/api/posts/` | ✅ Blog post added |
| **Read All** | GET | `/api/posts/` | ✅ See all posts |
| **Read One** | GET | `/api/posts/{id}/` | ✅ See one post |
| **Update** | PUT | `/api/posts/{id}/` | ✅ Post modified |
| **Delete** | DELETE | `/api/posts/{id}/` | ✅ Post removed |

---

## 📍 Section 7: Complete Blog Project - Wrapping Up

**⏱️ Time: 10 minutes**

### Your Project Structure Now

```
your-blog/
├── config/                         # Django configuration
│   ├── __init__.py
│   ├── settings.py                # MongoDB config (edited)
│   ├── urls.py                    # Routes config (edited)
│   └── wsgi.py
│
├── apps/                           # All Django applications
│   └── blog/                      # Blog application
│       ├── __init__.py
│       ├── apps.py                # App config
│       ├── models.py              # Post model (CREATED)
│       ├── views.py               # 5 CRUD endpoints (CREATED)
│       └── urls.py                # Blog routes (CREATED)
│
├── scripts/
│   └── seed_data.py               # Sample data loader
│
├── tests/
│   └── test_api.py                # API tests
│
├── docs/                           # Workshop documentation
│   ├── slides.md
│   ├── FAQ.md
│   └── START_HERE.md
│
├── manage.py                       # Django management
├── requirements.txt                # Dependencies
└── .env                           # MongoDB URI & secrets
```

### Data Flow in Your Blog

```
1. CLIENT REQUEST
   └─ curl -X POST http://localhost:8000/api/posts/

2. DJANGO RECEIVES
   └─ config/urls.py finds route
   └─ Calls apps/blog/views.py create_post()

3. VIEW PROCESSES
   └─ Extracts title, content, author
   └─ Calls Post.objects.create()

4. DJANGO ORM
   └─ django-mongodb-backend translates to MongoDB
   └─ Sends to MongoDB database

5. MONGODB STORES
   └─ Creates document in 'posts' collection
   └─ Returns document with ID

6. RESPONSE BACK
   └─ View formats as JSON
   └─ Returns status, ID, message

7. CLIENT SEES
   └─ {"status": "success", "id": "...", ...}
```

### Quick Command Reference

```bash
# Start the project
python manage.py runserver

# Create a post
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{"title":"...", "content":"...", "author":"..."}'

# Get all posts
curl http://localhost:8000/api/posts/

# Get one post
curl http://localhost:8000/api/posts/[ID]/

# Update post
curl -X PUT http://localhost:8000/api/posts/[ID]/ \
  -H "Content-Type: application/json" \
  -d '{"title":"..."}'

# Delete post
curl -X DELETE http://localhost:8000/api/posts/[ID]/
```

### Troubleshooting Checklist

**Server won't start?**

- ✅ Check .env file has MONGODB_URI
- ✅ Check MongoDB Atlas connection string is correct
- ✅ Check Python version is 3.9+
- ✅ Try: `pip install -r requirements.txt`

**Can't create posts?**

- ✅ Server must be running
- ✅ Check syntax in curl command
- ✅ Ensure Content-Type header is set
- ✅ Check MongoDB is accessible

**Can't see posts?**

- ✅ CREATE a post first!
- ✅ Use correct post ID in URLs
- ✅ Check MongoDB connection

**Port 8000 in use?**

- ✅ Use different port: `python manage.py runserver 8001`

---

## 📍 Section 8: Next Steps & Resources

**⏱️ Time: 5 minutes**

### What You've Accomplished Today

✅ **Created a complete blog REST API** with Django + MongoDB
✅ **Implemented all CRUD operations** (Create, Read, Update, Delete)
✅ **Deployed on GitHub Codespace** (no local setup needed)
✅ **Built a database** with MongoDB Atlas
✅ **Tested all endpoints** with real curl commands
✅ **Understood how web APIs work** end-to-end

### Extending Your Blog

**Add Comments:**

- Create Comment model with post_id reference
- Add POST /api/posts/{id}/comments/
- Add GET /api/posts/{id}/comments/

**Add Search:**

- Use MongoDB search: `Post.objects.filter(title__icontains='search')`
- Create GET /api/posts/search/?q=keyword

**Add User Authentication:**

- Use Django's built-in User model
- Add login/logout endpoints
- Restrict post editing to author only

**Add Categories:**

- Add category field to Post model
- Filter by category: GET /api/posts/?category=tech

**Build a Frontend:**

- Use React, Vue, or vanilla JavaScript
- Point it to your API endpoints
- Create beautiful blog UI

### Recommended Learning Resources

| Resource | Purpose |
|----------|---------|
| [Django Docs](https://docs.djangoproject.com/) | Complete Django reference |
| [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) | Cloud database hosting |
| [django-mongodb-backend](https://github.com/mongodb-labs/django-mongodb-backend) | MongoDB Django integration |
| [pymongo](https://pymongo.readthedocs.io/) | MongoDB Python driver |
| [REST API Design](https://restfulapi.net/) | Best practices for APIs |

### Practice Exercises

1. **Add admin panel** — Let users manage posts in Django admin
2. **Add pagination** — Show 10 posts per page
3. **Add sorting** — Order by date, title, author
4. **Add validation** — Require title length > 5 chars
5. **Add timestamps** — Show when posts were created/updated
6. **Add caching** — Speed up repeated reads
7. **Add logging** — Track API requests
8. **Add tests** — Test all your endpoints

### Deployment Options

**Host on Cloud:**

- **Azure App Service** — Enterprise hosting
- **Heroku** — Simple deployment
- **AWS Elastic Beanstalk** — AWS hosting
- **DigitalOcean** — Affordable VPS

**Keep Using Codespace:**

- Free tier available
- Always-on environment
- No setup needed
- Accessible from anywhere

### Common Questions

**Q: How do I save my work?**
A: Use GitHub! Push your code to a repository.

**Q: Can I add more fields to the Post?**
A: Yes! Edit models.py, add the field, restart Django, and the schema updates automatically (MongoDB advantage!).

**Q: How do I deploy this to production?**
A: Set `DEBUG=False`, configure static files, use a production database, and deploy to cloud platform.

**Q: Can I use a frontend?**
A: Absolutely! Your API works with any frontend (React, Vue, Angular, etc.).

**Q: What if I need more functionality?**
A: Django has plugins for almost everything. Check [Django Packages](https://djangopackages.org/).

### Key Lessons Learned

1. **APIs are simple** — Just HTTP requests and JSON responses
2. **CRUD covers 80% of apps** — Most apps are just storing/retrieving data
3. **Django + MongoDB makes it easy** — Build in hours, not days
4. **MongoDB is flexible** — Change schemas anytime
5. **You're ready to build** — You have all the pieces now!

---

## 🎓 You're a Web Developer Now

**What you learned:**
✓ How web applications actually work  
✓ How to build a production API  
✓ How to work with databases  
✓ How to think like a developer  

**Next: Pick a project and build it!**

Start with blog modifications, then build something completely new. The skills transfer directly.

---

### Workshop Feedback

We'd love to hear from you!

- What was confusing?
- What could be clearer?
- What would you build next?
- Any questions we missed?

**Thank you for attending!** 🚀
