# Django + MongoDB Workshop - Makefile

.PHONY: help install serve test seed clean slides slides-html slides-pdf

help:
	@echo "Django + MongoDB Workshop - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install      Install Python dependencies"
	@echo "  make serve        Start the development server"
	@echo "  make seed         Load sample data into MongoDB"
	@echo "  make test         Run API tests"
	@echo "  make test-curl    Test API with curl commands"
	@echo "  make shell        Open Django shell"
	@echo ""
	@echo "Presentation (Marp):"
	@echo "  make slides       Show slides in Marp live editor"
	@echo "  make slides-html  Export slides to HTML"
	@echo "  make slides-pdf   Export slides to PDF"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        Remove cache and generated files"
	@echo ""

install:
	pip install -r requirements.txt

serve:
	python manage.py runserver 0.0.0.0:8000

seed:
	python manage.py ingest

test:
	python tests/test_api.py

test-curl:
	@echo "Testing CREATE endpoint..."
	@curl -X POST http://localhost:8000/api/posts/ \
	  -H "Content-Type: application/json" \
	  -d '{"title":"Makefile Test","content":"Testing via Makefile","author":"Test User"}' | python -m json.tool
	@echo "\n"
	@echo "Testing READ endpoint..."
	@curl http://localhost:8000/api/posts/ | python -m json.tool

shell:
	python manage.py shell

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov 2>/dev/null || true

slides:
	@echo "🎨 Opening Marp slide editor..."
	@marp docs/slides.md

slides-html:
	@echo "📄 Exporting slides to HTML..."
	@marp docs/slides.md --html -o docs/slides.html
	@echo "✓ Slides exported to docs/slides.html"

slides-pdf:
	@echo "📕 Exporting slides to PDF..."
	@marp docs/slides.md -o docs/slides.pdf
	@echo "✓ Slides exported to docs/slides.pdf"

.DEFAULT_GOAL := help
