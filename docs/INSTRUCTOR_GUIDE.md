# Workshop Instructor Guide

## Django + MongoDB CRUD Workshop for Beginners

An excellent resource for conducting a 1-hour introduction to web development with Django and MongoDB.

---

## Workshop Overview

**Duration:** 60 minutes  
**Target Audience:** Non-technical, complete beginners  
**Difficulty:** Beginner-friendly  

### Workshop Components

1. **Presentation Slides** (`slides.md`)
   - 8 professional sections
   - Timing markers for each section
   - Real-world analogies and examples
   - Code snippets integrated throughout

2. **Live Demo Environment**
   - Complete Django + MongoDB project
   - Ready-to-run on GitHub Codespace
   - All CRUD operations implemented
   - Sample data included

3. **API Testing Tools**
   - `test_api.py` — Automated testing script
   - `Makefile` — Quick command shortcuts
   - curl examples — For live demos

---

## Pre-Workshop Setup (15 minutes before)

### Option 1: GitHub Codespace (Recommended for Online Workshops)

1. Navigate to the repository
2. Click **"Code"** → **"Codespaces"** → **"Create codespace on main"**
3. Wait for environment to load (1-2 minutes)
4. Open terminal and run:

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

5. Application is ready at `http://localhost:8000/`

### Option 2: Local Machine

```bash
# Install dependencies
pip install -r requirements.txt

# Option A: Use MongoDB Atlas (Cloud) - Recommended
# Update .env with your MongoDB Atlas connection string
# MONGODB_URI=mongodb+srv://username:password@cluster0.mongodb.net/blog_db?retryWrites=true&w=majority

# Option B: Use Local MongoDB
# Make sure it's running:
mongod --dbpath /data/db &

# Start Django
python manage.py runserver
```

---

## Detailed Workshop Timeline

### 0:00 - 0:05 | Section 1: Introduction (5 minutes)

**Slides:** Section 1 - What is Django & MongoDB?

**Objectives:**

- Demystify Django and MongoDB for non-technical audience
- Explain web frameworks as "toolboxes"
- Introduce the real-world analogy (filing cabinet)

**Key Points to Emphasize:**

- Django is like a helpful assistant
- MongoDB is flexible, like a notebook instead of a spreadsheet
- Both are used by real companies at scale

**Live Demo:**

- Show browser window with the API running
- Make a simple request to show something works
- Mention they'll understand this before the end of the workshop

---

### 0:05 - 0:10 | Section 2: Installation & Setup (5 minutes)

**Slides:** Section 2 - Installation & Setup

**Objectives:**

- Show how easy it is to get started
- Demystify installation process

**Key Points:**

- Everything is pre-configured (no setup headaches)
- In a real classroom, this part takes 30 minutes, but we've simplified it
- Show the requirements.txt file briefly

**Live Demo:**

- Show that Python dependencies are installed
- Show the .env file configuration
- Mention they could do this on their laptop later

---

### 0:10 - 0:20 | Section 3: Understanding CRUD (10 minutes)

**Slides:** Section 3 - Understanding CRUD Operations

**Critical Section:** This is where understanding crystallizes

**Teaching Strategy:**

1. Start with what CRUD means (Create, Read, Update, Delete)
2. Use the Blog Post analogy - very relatable
3. Show the Post model structure step-by-step
4. Explain APIs as "telephones to database"

**Interactive Element:**

- Ask the audience: "Who has ever created a post on social media?" (CREATE)
- "Who has ever read a post?" (READ)
- "Who has edited a post they made?" (UPDATE)
- "Who has deleted a post?" (DELETE)

**Key Points:**

- Every app they use does CRUD operations
- These are universal concepts across all programming
- Understanding CRUD = understanding 80% of web development

**Live Demo:**

- Don't do anything yet
- Just point to the blog model: "This is the structure we'll be working with"

---

### 0:20 - 0:30 | Section 4: Live Demo - CREATE (10 minutes)

**Slides:** Section 4 - Live Demo: CREATE Operation

**Objectives:**

- Show how to add data
- First hands-on experience
- Build confidence

**Live Demo Steps:**

1. **Show the Code** (2 minutes)
   - Display the `create_post` view in `blog/views.py`
   - Point out the three main parts:
     - Receiving data from the user
     - Saving to MongoDB
     - Sending back a response
   - Code is well-commented, so just highlight the comments

2. **Run a CURL Command** (3 minutes)

   ```bash
   curl -X POST http://localhost:8000/api/posts/ \
     -H "Content-Type: application/json" \
     -d '{
       "title": "My First Post",
       "content": "Hello World! This is my first blog post.",
       "author": "Alice"
     }'
   ```

   - Explain what each part does
   - Show the JSON response
   - Highlight: "The database returned an ID - that's how we know it worked!"

3. **Key Insight** (1 minute)
   - "The computer took our information and saved it to MongoDB"
   - "MongoDB gave it an ID so we can find it later"
   - "The API sent us back what we created as proof"

**Expected Audience Reaction:**

- "Wow, it actually worked!"
- Relief that it's not overly complicated

---

### 0:30 - 0:40 | Section 5: Live Demo - READ (10 minutes)

**Slides:** Section 5 - Live Demo: READ Operation

**Objectives:**

- Show how to retrieve data
- Show the power of databases
- Build on success from CREATE demo

**Live Demo Steps:**

1. **Show the Code** (2 minutes)
   - Display both `list_posts` and `get_post` views
   - Point out: "We wrote LESS code here than CREATE"
   - MongoDB does the hard work finding data

2. **Demo: Read All Posts** (3 minutes)

   ```bash
   curl http://localhost:8000/api/posts/
   ```

   - Show the JSON response with all posts
   - "See? MongoDB found everything and returned it as JSON"
   - If you have sample data, you'll see multiple results here

3. **Demo: Read One Post** (3 minutes)

   ```bash
   curl http://localhost:8000/api/posts/507f1f77bcf86cd799439011/
   ```

   - Using the ID from the CREATE demo
   - "We asked for one specific post by ID"
   - "MongoDB found exactly what we wanted"

4. **Key Insight** (2 minutes)
   - "Retrieving data is easier than creating it"
   - "MongoDB is fast at finding things"
   - "This is what happens when you load social media - it READs data"

---

### 0:40 - 0:55 | Section 6: Live Demo - UPDATE & DELETE (15 minutes)

**Slides:** Section 6 - Live Demo: UPDATE & DELETE Operations

**Objectives:**

- Complete the CRUD circle
- Show data can change and be removed
- Do a full cycle with one blog post

**Live Demo Steps:**

1. **Show the Code** (2 minutes)
   - Display `update_post` view
   - Mention: "Very similar to CREATE, but we're modifying existing data"
   - Display `delete_post` view
   - "This one is shortest because we're just removing something"

2. **Demo: Update a Post** (4 minutes)

   ```bash
   curl -X PUT http://localhost:8000/api/posts/507f1f77bcf86cd799439011/ \
     -H "Content-Type: application/json" \
     -d '{
       "title": "My Updated First Post",
       "content": "Hello World! This post has been updated."
     }'
   ```

   - Show the updated response
   - Point out: "The updated_at timestamp changed"
   - "This is what happens when you edit a social media post"

3. **Demo: Get After Update** (2 minutes)

   ```bash
   curl http://localhost:8000/api/posts/507f1f77bcf86cd799439011/
   ```

   - "Proof that it was updated"
   - "The content is different now"

4. **Demo: Delete a Post** (4 minutes)

   ```bash
   curl -X DELETE http://localhost:8000/api/posts/507f1f77bcf86cd799439011/
   ```

   - Show success response
   - Try to read again:

     ```bash
     curl http://localhost:8000/api/posts/507f1f77bcf86cd799439011/
     ```

   - "It's gone! This is what happens when you delete a post"
   - "You can't recover it - so be careful with deletion!"

5. **Full Circle Moment** (3 minutes)
   - "You've now seen all CRUD operations"
   - "In just 10 minutes, you understand what takes years to master"
   - "Every app you use does exactly this"

---

### 0:55 - 1:00 | Section 7-8: Q&A and Resources (5 minutes)

**Slides:** Section 7-8 - Putting It Together & Q&A

**Objectives:**

- Answer questions
- Point to resources
- Leave them excited to learn more

**Key Talking Points:**

- "You now understand the foundation of web development"
- "What you learned here applies to building any web app"
- "The hard part isn't the code - it's thinking about what to build"

**Questions to Ask Them:**

- "What would you want to build with these tools?"
- "Who wants to extend this project?"
- "Any questions about the code?"

**Resources to Share:**

- MongoDB documentation link
- Django documentation link
- RESTful API best practices
- Next steps to continue learning

---

## Demo Environment Safety Features

### What's Pre-Configured

- ✓ Django installed and working
- ✓ MongoDB running (on Codespace)
- ✓ Sample data loaded (optional)
- ✓ All CRUD endpoints working
- ✓ Error handling implemented

### What Could Go Wrong (and fixes)

| Issue | Solution |
|-------|----------|
| MongoDB not running | Restart it: `mongod --dbpath /data/db` |
| Port 8000 in use | Use different port: `python manage.py runserver 8001` |
| Dependencies missing | Run: `pip install -r requirements.txt` |
| Responses slow | Might need to restart MongoDB or Django |

---

## Alternative Format: Hands-On Workshop

If you want participants to code along:

1. **Setup Phase** (5 min)
   - Everyone clones the repo
   - Everyone installs dependencies
   - Everyone starts their Django server

2. **Learning Phase** (40 min)
   - Follow sections 1-6 together
   - Stop at each demo to let them try curl commands
   - Fix issues as they arise

3. **Experimentation Phase** (15 min)
   - Let them modify the code
   - Add new fields to Post model
   - Create new API endpoints
   - Test changes immediately

---

## Tips for Success

1. **Go Slow on Concepts**
   - Non-technical people need time to absorb ideas
   - Repeat key concepts multiple times
   - Use different metaphors if something doesn't land

2. **Show Real Impact**
   - Every CURL command = something visible happens
   - This builds confidence and engagement
   - Make it dramatic (it works!)

3. **Manage Time Strictly**
   - Don't spend more than 10 minutes on intro
   - Live demos are where the magic happens
   - Q&A at end, not in middle

4. **Have Backup Plans**
   - If internet is slow, pre-load pages
   - Have terminal window ready to go
   - Have code snippets saved
   - Have second laptop as backup

5. **Make It Personal**
   - Use names and examples from audience
   - Ask questions and listen
   - Show genuine excitement about technology

---

## After the Workshop

### For Participants Who Want to Continue

1. **Run Locally**
   - Clone the repo
   - Follow README.md
   - Modify and experiment

2. **Learn More**
   - MongoDB tutorials
   - Django tutorials
   - Build a real project

3. **Try Extensions**
   - Add user authentication
   - Add comments to posts
   - Add categories/tags
   - Deploy to cloud

### For Instructors

- Keep the slides.md file open during presentation
- Use the Makefile for quick commands
- Have test_api.py ready in a terminal
- Keep MongoDB running in background
- Have backup curl commands copied

---

## Success Metrics

### You've Succeeded If Participants

✓ Understand what CRUD means  
✓ Know it applies to every app they use  
✓ Can write a basic curl request  
✓ Understand how APIs work  
✓ Feel excited about web development  
✓ Know where to learn more  
✓ Believe *they could* build something like this  

### Bonus Points

✓ Participants clap or respond with enthusiasm  
✓ Participants ask smart follow-up questions  
✓ Participants want to continue learning  
✓ Participants try the code themselves afterward  

---

## Customization Options

### Make It Shorter (30 minutes)

- Skip environment setup explanation
- Do 3 demos instead of 5 (create, read one, delete)
- Focus on concepts over code details

### Make It Longer (2-3 hours)

- Have participants code along
- Have them modify the model
- Have them add new endpoints
- Deploy to cloud together

### Make It Domain-Specific

- Portfolio blog → Corporate blog
- Generic posts → Product reviews
- Anonymous authors → Team members
- Customize field names and examples

---

## Resources for Instructors

- **Django Docs**: <https://docs.djangoproject.com/>
- **MongoDB Docs**: <https://www.mongodb.com/docs/>
- **REST API Best Practices**: <https://restfulapi.net/>
- **Beginner Python**: <https://www.python.org/about/gettingstarted/>

## Questions?

If you run into issues with the workshop content, check:

1. README.md - has troubleshooting section
2. Code comments in views.py - explains each function
3. Test examples in test_api.py - shows all endpoints
4. This guide - has timing and strategy info

---

**Happy Teaching!** 🎓

The goal isn't to make experts, it's to spark curiosity and show that web development is learnable.
