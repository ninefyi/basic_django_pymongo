# Frequently Asked Questions (FAQ)

## About the Workshop

### Q: Is this really for beginners with no programming experience?

**A:** Yes! The workshop assumes ZERO programming knowledge. We explain even basic concepts like what HTTP is, what JSON looks like, and why databases exist. Participants just need curiosity.

### Q: Can non-technical people understand this?

**A:** Absolutely. We use real-world analogies (filing cabinets, post-it notes, helping assistants) to explain technical concepts. If you've ever written a blog post or edited something online, you understand CRUD operations.

### Q: How much time do I need to prepare as an instructor?

**A:**

- 30 minutes to review slides and instructor guide
- 15 minutes to test the code (run on Codespace)
- 5 minutes to set up demo environment
- **Total: ~50 minutes of prep**

### Q: Can I customize this for my audience?

**A:** Completely! The code is flexible. You can change:

- Model fields (e.g., Products instead of Posts)
- Examples (e.g., your company's use case)
- Length (make it 30 min, 1 hour, or 3 hours)
- Difficulty (add advanced topics after)

---

## Technical Questions

### Q: Do I need to install anything locally?

**A:** Not for Codespace! Everything is pre-configured. Just need a GitHub account. For local setup, you need Python, MongoDB, and the dependencies in requirements.txt.

### Q: What if I don't want to use MongoDB Atlas?

**A:** Your options:

1. Use local MongoDB (Codespace includes it)
2. Download MongoDB Community Edition
3. Use MongoDB Cloud free tier
4. Use Docker to run MongoDB

### Q: Can I use this with PostgreSQL or MySQL instead?

**A:** Yes! We already use Django ORM (django-mongodb-backend), which is
database-agnostic. To switch databases, just change the DATABASES configuration
in settings.py to use 'django.db.backends.postgresql' or 'django.db.backends.mysql'.
The model code stays the same.

### Q: Does this work on Windows, Mac, and Linux?

**A:** Yes to all! Codespace works on any platform through the browser. For local: Python and MongoDB work on all three major OS.

### Q: What's the minimum Python version needed?

**A:** Python 3.9+. We use Python 3.11 in Codespace, which is current and stable.

---

## Timing Questions

### Q: What if I only have 30 minutes?

**A:**

- Skip Section 2 (setup) — 5 min saved
- Combine Sections 3 & 4 — 3 min saved
- Demo only CREATE and READ operations
- Skip UPDATE/DELETE until Q&A
- **Result: 30-minute "CRUD Highlights" workshop**

### Q: Can I extend this to a full course?

**A:** Yes! After this foundation, you could add:

- **Week 2:** Add user authentication
- **Week 3:** Build a frontend with HTML/CSS/JavaScript
- **Week 4:** Add comments and relationships
- **Week 5:** Deploy to the cloud
- **Week 6:** Advanced features (search, pagination, etc.)

This workshop is an excellent foundation for a multi-week course.

### Q: How long are the live demos really?

**A:** Actual time in terminal: 2-3 minutes each. But with explanation and audience engagement, we allocate 10 minutes per demo section to answer questions and let it sink in.

---

## Audience Questions

### Q: Can I use this for high school students?

**A:** Yes! The concepts are universal. Adjust your examples to things they care about (social media, gaming, etc.).

### Q: Can I use this for corporate workshops?

**A:** Definitely! Use business-relevant examples (product catalogs, customer databases). The technology is the same, just the context changes.

### Q: What if people have different skill levels?

**A:** The workshop is designed for beginners, but intermediate developers can:

- Help troubleshoot others
- Suggest extensions to the code
- Ask deeper questions during Q&A
- Begin adding features during free time

### Q: Can people learn this asynchronously (self-paced)?

**A:** Yes! The README.md is complete enough for self-study. Participants can:

1. Follow the README step-by-step
2. Try each API endpoint themselves
3. Modify the code and experiment
4. Refer to docs for questions

- The only thing they miss is real-time Q&A

---

## Code Questions

### Q: Can I modify the Post model?

**A:** Yes! Follow this pattern:

1. Edit `blog/models.py` — add/remove fields
2. Update `blog/views.py` — adjust validation if needed
3. Update `seed_data.py` — create relevant sample data
4. Update slides with new model structure

Example: Change from Blog Posts to Product Reviews by renaming fields.

### Q: How do I add a new endpoint (like search)?

**A:** Add to `blog/views.py`:

```python
@require_http_methods(["GET"])
def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects(title__icontains=query)
    # Format and return as JSON
```

Then add to `blog/urls.py`:

```python
path('posts/search/', search_posts, name='search_posts'),
```

### Q: Can I add user authentication?

**A:** Yes, but it expands the workshop. You'd use Django's built-in authentication:

- `django.contrib.auth` for user management
- Middleware for login checking
- Token authentication for APIs

This would be a good "Week 2" feature.

### Q: How do I deploy this to production?

**A:** Several options:

- **Azure App Service** — Deploy and run Django
- **AWS Elastic Beanstalk** — Similar to App Service
- **Heroku** — Easy deployment
- **Docker** — Container deployment

Basics:

1. Set `DEBUG=False` in settings.py
2. Update ALLOWED_HOSTS
3. Use strong SECRET_KEY
4. Set up environment variables
5. Point to MongoDB Atlas (not local)

---

## Troubleshooting

### Q: The server won't start. What now?

**A:** Check in order:

1. Are you in the right directory? (`pwd` should show project folder)
2. Are dependencies installed? (`pip list | grep Django`)
3. Is Python the right version? (`python --version` should be 3.9+)
4. Are there syntax errors? (Check error message carefully)

Run this to reset:

```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
python manage.py runserver
```

### Q: "Cannot connect to MongoDB" error

**A:**

1. Is MongoDB running? Try: `mongod --dbpath /data/db`
2. Is the URI correct in `.env`?
3. Can you access MongoDB? Try: `mongosh` or `mongo` command
4. If using Atlas, copy the connection string exactly

### Q: "Module not found" errors

**A:** Install missing dependency:

```bash
pip install [module-name]
pip freeze > requirements.txt  # Update requirements
```

### Q: Port 8000 is already in use

**A:** Use different port:

```bash
python manage.py runserver 8001
# Or find what's using 8000:
lsof -i :8000
kill [PID]
```

### Q: Curl commands don't work

**A:** Make sure:

- Django server is running
- You're using correct URL (<http://localhost:8000>, not https)
- Header `-H "Content-Type: application/json"` is included for POST/PUT
- Post ID is valid (from a previous CREATE response)

### Q: Sample data won't load

**A:** Check:

```bash
# Verify MongoDB is running
mongod --dbpath /data/db

# Check connection error
python seed_data.py

# Check data was created
python manage.py shell
>>> from blog.models import Post
>>> Post.objects.count()
```

---

## Learning Path

### If this is their first time

1. Attend workshop (1 hour)
2. Try examples themselves (1 hour)
3. Modify the Post model (1 hour)
4. Add a new endpoint (2 hours)
5. Tackle: "Could I use this for [my idea]?"

### If they want to continue

1. Add authentication (Week 2)
2. Build a frontend (Week 3)
3. Deploy to cloud (Week 4)
4. Add more complex features

### If they hit a wall

1. Check the code comments
2. Read Django documentation
3. Search Stack Overflow (most questions are already answered)
4. Ask in community forums

---

## Advanced Topics (Not in Workshop)

These are good follow-ups for interested participants:

**Database:**

- MongoDB aggregation pipelines
- Indexing and optimization
- Replication and sharding
- What happens at scale (millions of documents)

**Backend:**

- Authentication and authorization
- Middleware and decorators
- Testing (unit tests, integration tests)
- Caching and performance
- Background tasks and queues

**Frontend:**

- HTML/CSS/JavaScript basics
- React or Vue frameworks
- Connecting frontend to backend API
- CORS (Cross-Origin Resource Sharing)

**DevOps:**

- Docker containerization
- Kubernetes deployment
- CI/CD pipelines
- Monitoring and logging
- Scaling applications

---

## One-Sentence Answers

**Q: Is this too simple?**
A: No, it's appropriately complex for beginners and sets foundation for advanced topics.

**Q: Can I use this for my job training?**
A: Yes, it's production-quality code and documentation.

**Q: How often should I update this?**
A: Django and MongoDB update slowly; update annually or when dependencies change.

**Q: Can students modify and redistribute this?**
A: Check your license, but the concepts are universal and anyone should learn them.

**Q: What's the hardest part for beginners?**
A: Understanding why we need databases and how APIs communicate (we explain this well).

**Q: Will they know how to build an app after this?**
A: They'll know the core concepts and have a working example to modify.

---

## Contact & Support

### If code doesn't work

1. Check README.md troubleshooting
2. Verify environment setup
3. Check error message carefully
4. Search error on Stack Overflow
5. Read Django/MongoDB docs

### If workshop content needs adjustment

1. Modify slides.md directly
2. Update INSTRUCTOR_GUIDE.md with timing changes
3. Test changes before next workshop
4. Gather participant feedback

### If participants want to continue

- Share INSTRUCTOR_GUIDE.md "Next Steps" section
- Recommend the learning path above
- Point to official documentation
- Suggest building their own project

---

## Student Feedback You Might Get

**Positive Feedback:**

- "I never thought I could write code"
- "This actually makes sense!"
- "Can I build [my idea] with this?"
- "When's the next course?"

**Constructive Feedback:**

- "You went too fast during the API part" → Add Q&A breaks in Section 5-6
- "I wish I could have coded along" → Extend to 2-hour hands-on version
- "Can you explain the JSON format more?" → Add JSON explanation slide
- "Deploy this to the cloud?" → Great next-level workshop

**How to Respond:**

- **Positive:** Thank them, it energizes you!
- **Constructive:** Take notes, iterate, improve
- **Out of scope:** "Great question for next workshop!"

---

## You've Got This

The workshop is complete, tested, and ready. Questions come up in real time, and that's okay. You have:

✓ Clear slides with timing  
✓ Complete code that works  
✓ Troubleshooting guide  
✓ Teaching strategy  
✓ Example outputs  
✓ Q&A section  

**Trust the material. Enjoy the teaching. Have fun!** 🎓
