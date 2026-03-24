#!/bin/bash

# Django + MongoDB Workshop Setup Script for GitHub Codespace
# This script runs automatically when the Codespace/Container is created
# The Dockerfile has already installed all system dependencies

set -e

echo "🚀 Finalizing Django + MongoDB Workshop Setup..."

# Upgrade pip to latest version
echo "📦 Ensuring pip is up to date..."
pip install --upgrade pip --quiet

# Install/reinstall Python dependencies (in case requirements.txt was updated)
if [ -f requirements.txt ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt --quiet
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "  💡 Tip: Update .env with your MongoDB Atlas connection string"
fi

# Verify MongoDB is running
echo "🗄️  Checking MongoDB..."
mkdir -p /data/db /tmp/mongodb
if ! pgrep mongod > /dev/null; then
    echo "  Starting MongoDB service..."
    mongod --dbpath /data/db --logpath /tmp/mongodb/mongod.log --fork > /dev/null 2>&1 || echo "  MongoDB starting in background"
    sleep 2
else
    echo "  ✓ MongoDB is already running"
fi

# Verify Marp CLI is available
echo "🎨 Checking Marp CLI..."
if command -v marp &> /dev/null; then
    MARP_VERSION=$(marp --version 2>/dev/null || echo "unknown")
    echo "  ✓ Marp CLI is ready ($MARP_VERSION)"
else
    echo "  ⚠️  Marp CLI not found - installing now..."
    npm install -g @marp-team/marp-cli --quiet
fi

echo ""
echo "✅ Setup Complete!"
echo ""
echo "🎯 Quick Start Commands:"
echo ""
echo "1. Load sample data (optional):"
echo "   python scripts/seed_data.py"
echo ""
echo "2. Start the Django server:"
echo "   python manage.py runserver 0.0.0.0:8000"
echo ""
echo "3. Generate presentation from slides:"
echo "   marp docs/slides.md --html -o docs/slides.html"
echo ""
echo "4. Test the API:"
echo "   curl http://localhost:8000/api/posts/"
echo ""
echo "📖 Documentation:"
echo "   - docs/START_HERE.md      - Project overview"
echo "   - README.md               - Complete API documentation"
echo "   - docs/INSTRUCTOR_GUIDE.md - Workshop teaching guide"
echo "   - docs/slides.md          - Workshop presentation (markdown)"
echo ""

