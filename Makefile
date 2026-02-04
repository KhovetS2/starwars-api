.PHONY: help install dev test lint format run docker-up docker-down docker-build docker-logs clean

# Default target
help:
	@echo "🌌 Star Wars API - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install     Install production dependencies"
	@echo "  make dev         Install development dependencies"
	@echo "  make run         Run the API locally (requires MongoDB)"
	@echo "  make test        Run all tests"
	@echo "  make lint        Run linter (ruff)"
	@echo "  make format      Format code (black)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up   Start API and MongoDB with Docker Compose"
	@echo "  make docker-down Stop Docker containers"
	@echo "  make docker-build Build Docker image"
	@echo "  make docker-logs View Docker container logs"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean       Remove cache and build files"

# Development
install:
	pip install -e .

dev:
	pip install -e ".[dev]"

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest test/ -v

test-cov:
	pytest test/ -v --cov=app --cov-report=term-missing

lint:
	ruff check app/ test/

format:
	black app/ test/
	ruff check app/ test/ --fix

# Docker
docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-build:
	docker compose build

docker-logs:
	docker compose logs -f

docker-restart:
	docker compose restart

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
