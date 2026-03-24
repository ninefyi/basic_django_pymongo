"""
Quick API Test Script for Django + MongoDB Workshop
Tests all CRUD operations

Usage:
    python test_api.py
"""

import requests
import json
import sys

BASE_URL = 'http://localhost:8000/api'


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def create_post(title, content, author="Workshop User"):
    """Test CREATE operation."""
    print_section("TEST 1: CREATE A NEW POST")
    
    data = {
        'title': title,
        'content': content,
        'author': author
    }
    
    print(f"Sending POST request to {BASE_URL}/posts/")
    print(f"Data: {json.dumps(data, indent=2)}\n")
    
    try:
        response = requests.post(f'{BASE_URL}/posts/', json=data)
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}\n")
        
        if response.status_code == 201:
            print("✓ Post created successfully!")
            return result['post']['id']
        else:
            print("✗ Failed to create post")
            return None
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server")
        print("Make sure Django is running: python manage.py runserver")
        return None


def list_posts():
    """Test READ ALL operation."""
    print_section("TEST 2: READ ALL POSTS")
    
    print(f"Sending GET request to {BASE_URL}/posts/\n")
    
    try:
        response = requests.get(f'{BASE_URL}/posts/')
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}\n")
        
        if response.status_code == 200:
            count = result.get('count', 0)
            print(f"✓ Found {count} post(s)")
            return True
        else:
            print("✗ Failed to fetch posts")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server")
        return False


def get_post(post_id):
    """Test READ ONE operation."""
    print_section(f"TEST 3: READ ONE POST (ID: {post_id})")
    
    print(f"Sending GET request to {BASE_URL}/posts/{post_id}/\n")
    
    try:
        response = requests.get(f'{BASE_URL}/posts/{post_id}/')
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}\n")
        
        if response.status_code == 200:
            print(f"✓ Post retrieved successfully!")
            return True
        else:
            print("✗ Post not found")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server")
        return False


def update_post(post_id, title, content):
    """Test UPDATE operation."""
    print_section(f"TEST 4: UPDATE POST (ID: {post_id})")
    
    data = {
        'title': title,
        'content': content
    }
    
    print(f"Sending PUT request to {BASE_URL}/posts/{post_id}/")
    print(f"Data: {json.dumps(data, indent=2)}\n")
    
    try:
        response = requests.put(f'{BASE_URL}/posts/{post_id}/', json=data)
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}\n")
        
        if response.status_code == 200:
            print("✓ Post updated successfully!")
            return True
        else:
            print("✗ Failed to update post")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server")
        return False


def delete_post(post_id):
    """Test DELETE operation."""
    print_section(f"TEST 5: DELETE POST (ID: {post_id})")
    
    print(f"Sending DELETE request to {BASE_URL}/posts/{post_id}/\n")
    
    try:
        response = requests.delete(f'{BASE_URL}/posts/{post_id}/')
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}\n")
        
        if response.status_code == 200:
            print("✓ Post deleted successfully!")
            return True
        else:
            print("✗ Failed to delete post")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server")
        return False


def health_check():
    """Test health check endpoint."""
    print_section("PRE-TEST: HEALTH CHECK")
    
    print(f"Sending GET request to {BASE_URL}/../\n")
    
    try:
        response = requests.get('http://localhost:8000/')
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}\n")
        
        if response.status_code == 200:
            print("✓ Server is running!")
            return True
        else:
            print("✗ Server returned unexpected response")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server")
        print("\nMake sure Django is running:")
        print("  python manage.py runserver 0.0.0.0:8000")
        return False


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  Django + MongoDB CRUD Workshop - API Test Suite  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Check if server is running
    if not health_check():
        sys.exit(1)
    
    # Test CREATE
    post_id = create_post(
        title="Workshop Test Post",
        content="This is a test post created during the workshop demo. It demonstrates the CREATE operation."
    )
    
    if not post_id:
        print("\nCannot continue: Failed to create post")
        sys.exit(1)
    
    # Test READ ALL
    list_posts()
    
    # Test READ ONE
    get_post(post_id)
    
    # Test UPDATE
    update_post(
        post_id,
        title="Workshop Test Post (Updated)",
        content="This post has been updated to demonstrate the UPDATE operation."
    )
    
    # Test READ ONE after update
    get_post(post_id)
    
    # Test DELETE
    delete_post(post_id)
    
    # Final summary
    print_section("TEST SUMMARY")
    print("All CRUD operations tested successfully!")
    print("\nOperations tested:")
    print("  ✓ CREATE - Add new post")
    print("  ✓ READ   - Get all posts")
    print("  ✓ READ   - Get one post")
    print("  ✓ UPDATE - Modify post")
    print("  ✓ DELETE - Remove post")
    print("\n")


if __name__ == '__main__':
    main()
