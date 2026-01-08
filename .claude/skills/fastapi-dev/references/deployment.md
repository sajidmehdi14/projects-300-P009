# Docker Deployment Reference

## Table of Contents
- [Dockerfile](#dockerfile)
- [Docker Compose](#docker-compose)
- [Multi-stage Build](#multi-stage-build)
- [Environment Configuration](#environment-configuration)
- [Production Settings](#production-settings)
- [Health Checks](#health-checks)
- [Logging](#logging)

---

## Dockerfile

Basic Dockerfile:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY ./app ./app

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Docker Compose

```yaml
# docker-compose.yml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=false
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

Development compose:
```yaml
# docker-compose.dev.yml
version: "3.8"

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app  # Hot reload
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
      - DEBUG=true
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=app
```

---

## Multi-stage Build

```dockerfile
# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

---

## Environment Configuration

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "FastAPI App"
    debug: bool = False

    # Database
    database_url: str

    # Auth
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost:5432/app
SECRET_KEY=your-super-secret-key-at-least-32-characters
DEBUG=false
CORS_ORIGINS=["https://myapp.com","https://api.myapp.com"]
```

```bash
# .env.example (commit this, not .env)
DATABASE_URL=postgresql://user:pass@localhost:5432/app
SECRET_KEY=change-me-in-production
DEBUG=true
CORS_ORIGINS=["http://localhost:3000"]
```

---

## Production Settings

```python
# app/main.py
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    docs_url="/docs" if settings.debug else None,  # Disable docs in prod
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)
```

Gunicorn config:
```python
# gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 120
timeout = 120
graceful_timeout = 30
max_requests = 1000
max_requests_jitter = 50
```

Production Dockerfile with Gunicorn:
```dockerfile
CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
```

---

## Health Checks

```python
# app/routers/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.deps import get_db

router = APIRouter(tags=["health"])

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.get("/health/db")
def db_health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

@router.get("/ready")
def readiness_check(db: Session = Depends(get_db)):
    """Kubernetes readiness probe"""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Not ready")

@router.get("/live")
def liveness_check():
    """Kubernetes liveness probe"""
    return {"status": "alive"}
```

---

## Logging

```python
# app/core/logging.py
import logging
import sys
from app.core.config import settings

def setup_logging():
    log_level = logging.DEBUG if settings.debug else logging.INFO

    # JSON formatter for production
    if not settings.debug:
        import json

        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_obj = {
                    "timestamp": self.formatTime(record),
                    "level": record.levelname,
                    "message": record.getMessage(),
                    "module": record.module,
                }
                if record.exc_info:
                    log_obj["exception"] = self.formatException(record.exc_info)
                return json.dumps(log_obj)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
    else:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)

    # Reduce noise from libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# app/main.py
from app.core.logging import setup_logging

setup_logging()
```

Request logging middleware:
```python
import logging
import time
from fastapi import Request

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} duration={duration:.3f}s"
    )
    return response
```

---

## Docker Commands Cheatsheet

```bash
# Build
docker build -t myapp .

# Run
docker run -p 8000:8000 --env-file .env myapp

# Compose up
docker-compose up -d

# Compose with specific file
docker-compose -f docker-compose.dev.yml up

# View logs
docker-compose logs -f api

# Shell into container
docker-compose exec api /bin/bash

# Run migrations
docker-compose exec api alembic upgrade head

# Stop
docker-compose down

# Stop and remove volumes
docker-compose down -v
```
