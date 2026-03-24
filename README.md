# Django + MongoDB CRUD Workshop

A beginner-friendly workshop for learning CRUD operations (Create, Read, Update, Delete) using Django and MongoDB.

## What You'll Learn

- **Django Basics** — How web frameworks work
- **MongoDB Fundamentals** — Document-based data storage
- **CRUD Operations** — Managing data in databases
- **REST APIs** — How applications talk to each other
- **Real-World Development** — Building production-ready code

## Project Overview

```
Blog API
├── Create a new blog post (POST /api/posts/)
├── Read all posts (GET /api/posts/)
├── Read one post (GET /api/posts/{id}/)
├── Update a post (PUT /api/posts/{id}/)
└── Delete a post (DELETE /api/posts/{id}/)
```

## Quick Start

### Option 1: GitHub Codespace (Easiest)

1. Click **"Code"** → **"Codespaces"** → **"Create codespace on main"**
2. Wait for the environment to load (about 1-2 minutes)
3. Open a terminal and run:

```bash
# Start the Django development server
python manage.py runserver 0.0.0.0:8000
```

1. Open in browser: `http://localhost:8000/`

### Option 2: Local Machine

#### Requirements

- Python 3.9+
- MongoDB (local or MongoDB Atlas account)

#### Installation

```bash
# 1. Clone or download this repository
git clone <repository-url>
cd 20260328_basic_django

# 2. Create a virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env
# Edit .env and set your MONGODB_URI
```

#### Start Developing

```bash
# Load sample data (optional)
python seed_data.py

# Start the server
python manage.py runserver
```

Visit: `http://localhost:8000/`

## API Documentation

### 1. Create a Blog Post

**Request:**

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "Hello world! This is my first blog post.",
    "author": "Alice"
  }'
```

**Response:**

```json
{
  "status": "success",
  "message": "Post created successfully",
  "post": {
    "id": "507f1f77bcf86cd799439011",
    "title": "My First Post",
    "content": "Hello world! This is my first blog post.",
    "author": "Alice",
    "created_at": "2024-03-24T10:30:45.123456+00:00",
    "updated_at": "2024-03-24T10:30:45.123456+00:00"
  }
}
```

### 2. Read All Blog Posts

**Request:**

```bash
curl http://localhost:8000/api/posts/
```

**With filters:**

```bash
# Get posts by specific author
curl "http://localhost:8000/api/posts/?author=Alice"

# Limit results
curl "http://localhost:8000/api/posts/?limit=10"
```

**Response:**

```json
{
  "status": "success",
  "count": 1,
  "posts": [
    {
      "id": "507f1f77bcf86cd799439011",
      "title": "My First Post",
      "content": "Hello world! This is my first blog post.",
      "author": "Alice",
      "created_at": "2024-03-24T10:30:45.123456+00:00",
      "updated_at": "2024-03-24T10:30:45.123456+00:00"
    }
  ]
}
```

### 3. Read One Blog Post

**Request:**

```bash
curl http://localhost:8000/api/posts/507f1f77bcf86cd799439011/
```

**Response:**

```json
{
  "status": "success",
  "post": {
    "id": "507f1f77bcf86cd799439011",
    "title": "My First Post",
    "content": "Hello world! This is my first blog post.",
    "author": "Alice",
    "created_at": "2024-03-24T10:30:45.123456+00:00",
    "updated_at": "2024-03-24T10:30:45.123456+00:00"
  }
}
```

### 4. Update a Blog Post

**Request:**

```bash
curl -X PUT http://localhost:8000/api/posts/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Updated First Post",
    "content": "Hello world! This post has been updated."
  }'
```

**Response:**

```json
{
  "status": "success",
  "message": "Post updated successfully",
  "post": {
    "id": "507f1f77bcf86cd799439011",
    "title": "My Updated First Post",
    "content": "Hello world! This post has been updated.",
    "author": "Alice",
    "created_at": "2024-03-24T10:30:45.123456+00:00",
    "updated_at": "2024-03-24T10:35:20.654321+00:00"
  }
}
```

### 5. Delete a Blog Post

**Request:**

```bash
curl -X DELETE http://localhost:8000/api/posts/507f1f77bcf86cd799439011/
```

**Response:**

```json
{
  "status": "success",
  "message": "Post deleted successfully"
}
```

## Project Structure

```
blog-api/
├── slides.md                    # Workshop presentation slides
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management tool
├── settings.py                  # Django configuration
├── urls.py                      # Main URL routes
├── wsgi.py                      # Production config
├── seed_data.py                 # Create sample data
├── .env.example                 # Environment variables template
│
├── blog/                        # Blog application
│   ├── __init__.py
│   ├── models.py               # Post model (MongoDB)
│   ├── views.py                # CRUD endpoints
│   └── urls.py                 # Blog routes
│
└── .devcontainer/              # GitHub Codespace config
    ├── devcontainer.json
    └── setup.sh
```

## Data Model

### Post Document

```python
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),  # Unique ID
  "title": "My First Post",                      # Required
  "content": "Hello world...",                   # Required
  "author": "Alice",                             # Optional, default: "Anonymous"
  "created_at": ISODate("2024-03-24T10:30:45Z"), # Auto-set
  "updated_at": ISODate("2024-03-24T10:30:45Z")  # Auto-set
}
```

## Workshop Presentation with Marp

The workshop slides are written in **Marp** markdown format (`slides.md`). Marp allows you to create beautiful presentations from markdown.

### View Slides Live (Interactive Editor)

```bash
# Open Marp live editor
marp slides.md

# Or use Makefile
make slides
```

### Export Slides to HTML

```bash
# Generate standalone HTML presentation
marp slides.md --html -o slides.html

# Or use Makefile
make slides-html
```

Then open `slides.html` in your browser.

### Export Slides to PDF

```bash
# Generate PDF presentation (requires Chromium/Chrome)
marp slides.md -o slides.pdf

# Or use Makefile
make slides-pdf
```

### Edit Slides

The `slides.md` file contains:

- 8 professional sections
- Timing markers for each section
- Real-world analogies and examples
- Code snippets and demonstrations
- Ready for live presentation

Feel free to customize the slides for your specific audience and add your own examples!

## Troubleshooting

### "Cannot connect to MongoDB"

**Solution 1: Use MongoDB Atlas (Cloud) - Recommended**

1. Go to <https://www.mongodb.com/cloud/atlas>
2. Create a free account
3. Create a free M0 cluster
4. Get your connection string
5. Update `.env` file:

```
MONGODB_URI=mongodb+srv://username:password@cluster0.mongodb.net/blog_db?retryWrites=true&w=majority
```

**Solution 2: Use Local MongoDB**
Make sure MongoDB is running:

```bash
# Start MongoDB locally
mongod --dbpath /data/db
```

### "ModuleNotFoundError: No module named 'django_mongodb_backend'"

**Solution:** Install dependencies

```bash
pip install -r requirements.txt
```

### "POST/PUT not working"

**Ensure you're using the correct HTTP method and headers:**

```bash
# Always include Content-Type header for POST/PUT
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{"title": "..."}' 
```

### "Port 8000 already in use"

**Use a different port:**

```bash
python manage.py runserver 8001
```

## Testing with Python Requests

Create a `test_api.py` file:

```python
import requests
import json

BASE_URL = 'http://localhost:8000/api'

# CREATE
def create_post():
    data = {
        'title': 'Test Post',
        'content': 'This is a test',
        'author': 'Test User'
    }
    response = requests.post(f'{BASE_URL}/posts/', json=data)
    print('CREATE:', response.json())
    return response.json()['post']['id']

# READ ALL
def list_posts():
    response = requests.get(f'{BASE_URL}/posts/')
    print('READ ALL:', response.json())

# READ ONE
def get_post(post_id):
    response = requests.get(f'{BASE_URL}/posts/{post_id}/')
    print('READ ONE:', response.json())

# UPDATE
def update_post(post_id):
    data = {'title': 'Updated Title'}
    response = requests.put(f'{BASE_URL}/posts/{post_id}/', json=data)
    print('UPDATE:', response.json())

# DELETE
def delete_post(post_id):
    response = requests.delete(f'{BASE_URL}/posts/{post_id}/')
    print('DELETE:', response.json())

# Test all operations
if __name__ == '__main__':
    post_id = create_post()
    list_posts()
    get_post(post_id)
    update_post(post_id)
    delete_post(post_id)
```

Run it:

```bash
pip install requests
python test_api.py
```

## Next Steps

1. **Try the API** — Test all CRUD operations
2. **Modify Data** — Add fields to the Post model
3. **Add Validation** — Validate user input
4. **Add Authentication** — Secure your API
5. **Deploy to Cloud** — Deploy to Azure, AWS, or Heroku

## Learning Resources

- **MongoDB + Django**: <https://www.mongodb.com/docs/languages/python/django-mongodb/>
- **Django Documentation**: <https://docs.djangoproject.com/>
- **REST API Design**: <https://restfulapi.net/>
- **MongoDB Atlas**: <https://www.mongodb.com/cloud/atlas>

## Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
# Django settings
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True

# MongoDB connection
# Local: mongodb://localhost:27017/blog_db
# Atlas: mongodb+srv://user:password@cluster.mongodb.net/blog_db
MONGODB_URI=mongodb://localhost:27017/blog_db
```

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Load sample data
python seed_data.py

# Start development server
python manage.py runserver

# Open Django shell for testing
python manage.py shell

# Run tests (add your own)
python manage.py test
```

## Support

For questions or issues:

1. Check the **Troubleshooting** section above
2. Review code comments in `blog/views.py`
3. Read the Django documentation
4. Check MongoDB documentation

## License

This workshop material is provided for educational purposes.

---

**Happy Coding!** 🚀
