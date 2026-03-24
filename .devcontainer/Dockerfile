# Django + MongoDB CRUD Workshop Development Container
# Supports GitHub Codespace with Python, Node.js, MongoDB, and Marp

FROM mcr.microsoft.com/devcontainers/base:jammy

# Install Python 3.11
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Upgrade pip
RUN python -m pip install --upgrade pip setuptools wheel

# Install Node.js (required for Marp CLI)
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Marp CLI globally
RUN npm install -g @marp-team/marp-cli

# Install additional system utilities
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    jq \
    make \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Install Python requirements at build time (can be overridden at runtime)
COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NODE_ENV=production

# Expose ports for development
EXPOSE 8000 3000

# Create a startup script for the container
RUN echo '#!/bin/bash\n\
set -e\n\
echo "🚀 Django + MongoDB Atlas Workshop Container Started"\n\
\n\
# Create .env if it doesn'\''t exist\n\
if [ ! -f .env ]; then\n\
    echo "📝 Creating .env file from template..."\n\
    cp .env.example .env\n\
    echo "⚠️  Please configure MONGODB_URI in .env with your MongoDB Atlas connection string"\n\
fi\n\
\n\
echo "✅ Container ready!"\n\
echo ""\n\
echo "💡 Quick commands:"\n\
echo "   python manage.py runserver 0.0.0.0:8000"\n\
echo "   python seed_data.py"\n\
echo "   marp slides.md --html"\n\
echo ""\n\
echo "📖 MongoDB Atlas Setup:"\n\
echo "   1. Create free cluster: https://account.mongodb.com/account"\n\
echo "   2. Get connection string from Atlas"\n\
echo "   3. Add it to .env as MONGODB_URI"\n\
echo ""\n\
echo "📖 Documentation:"\n\
echo "   See README.md and START_HERE.md"\n\
echo ""\n\
\n\
exec "$@"' > /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
