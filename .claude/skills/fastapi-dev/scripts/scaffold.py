#!/usr/bin/env python3
"""
FastAPI Project Scaffolding Script

Creates a production-ready FastAPI project structure with optional features.

Usage:
    python scaffold.py <project_name> [--path <output_path>] [options]

Options:
    --auth          Include JWT authentication
    --db            Include PostgreSQL database setup
    --docker        Include Docker configuration
    --full          Include all features (auth, db, docker)

Examples:
    python scaffold.py myapi
    python scaffold.py myapi --path /projects --full
    python scaffold.py myapi --auth --docker
"""

import argparse
import os
import sys
from pathlib import Path

def create_file(path: Path, content: str):
    """Create a file with the given content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n")
    print(f"  ✓ Created {path}")

def scaffold_project(name: str, output_path: Path, include_auth: bool, include_db: bool, include_docker: bool):
    """Scaffold a FastAPI project."""
    project_dir = output_path / name

    if project_dir.exists():
        print(f"Error: Directory {project_dir} already exists")
        sys.exit(1)

    print(f"\n🚀 Creating FastAPI project: {name}")
    print(f"   Location: {project_dir}\n")

    # Main application
    main_imports = ["from fastapi import FastAPI"]
    main_middleware = ""
    main_routers = ""

    if include_auth or include_db:
        main_imports.append("from app.core.config import settings")

    if include_db:
        main_imports.append("from contextlib import asynccontextmanager")
        main_imports.append("from app.core.database import engine, Base")

    if include_auth:
        main_routers += "\nfrom app.routers import auth\napp.include_router(auth.router)"

    main_content = f'''
{chr(10).join(main_imports)}
from fastapi.middleware.cors import CORSMiddleware

{"@asynccontextmanager" if include_db else ""}
{"async def lifespan(app: FastAPI):" if include_db else ""}
{"    Base.metadata.create_all(bind=engine)" if include_db else ""}
{"    yield" if include_db else ""}

app = FastAPI(
    title="{name}",
    description="FastAPI application",
    version="0.1.0",
    {"lifespan=lifespan," if include_db else ""}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {{"message": "Hello World"}}

@app.get("/health")
def health():
    return {{"status": "healthy"}}
{main_routers}
'''
    create_file(project_dir / "app" / "main.py", main_content)

    # __init__.py files
    create_file(project_dir / "app" / "__init__.py", "")
    create_file(project_dir / "app" / "routers" / "__init__.py", "")
    create_file(project_dir / "app" / "schemas" / "__init__.py", "")
    create_file(project_dir / "app" / "core" / "__init__.py", "")

    if include_db:
        create_file(project_dir / "app" / "models" / "__init__.py", "")
        create_file(project_dir / "app" / "crud" / "__init__.py", "")

    # Config
    config_content = f'''
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "{name}"
    debug: bool = True
    {"database_url: str = \"postgresql://postgres:postgres@localhost:5432/{name}\"" if include_db else ""}
    {"secret_key: str = \"your-secret-key-change-in-production\"" if include_auth else ""}
    {"algorithm: str = \"HS256\"" if include_auth else ""}
    {"access_token_expire_minutes: int = 30" if include_auth else ""}

    model_config = {{
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }}

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
'''
    create_file(project_dir / "app" / "core" / "config.py", config_content)

    # Database setup
    if include_db:
        db_content = '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
        create_file(project_dir / "app" / "core" / "database.py", db_content)

        # Example model
        user_model = '''
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
'''
        create_file(project_dir / "app" / "models" / "user.py", user_model)

    # Auth setup
    if include_auth:
        security_content = '''
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
'''
        create_file(project_dir / "app" / "core" / "security.py", security_content)

        deps_content = '''
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Annotated
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {"user_id": user_id, "username": payload.get("username")}
    except JWTError:
        raise credentials_exception
'''
        create_file(project_dir / "app" / "core" / "deps.py", deps_content)

        auth_router = '''
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel

from app.core.security import create_access_token, verify_password, get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Placeholder - integrate with your database
fake_users_db = {}

@router.post("/register", response_model=Token)
def register(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")

    fake_users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "hashed_password": get_password_hash(user.password),
    }

    access_token = create_access_token(data={"sub": 1, "username": user.username})
    return Token(access_token=access_token)

@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": 1, "username": user["username"]})
    return Token(access_token=access_token)
'''
        create_file(project_dir / "app" / "routers" / "auth.py", auth_router)

    # Example router
    items_router = '''
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["items"])

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

items_db = []

@router.get("/")
def list_items():
    return items_db

@router.get("/{item_id}")
def get_item(item_id: int):
    if item_id < 0 or item_id >= len(items_db):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@router.post("/")
def create_item(item: Item):
    items_db.append(item.model_dump())
    return {"id": len(items_db) - 1, **item.model_dump()}
'''
    create_file(project_dir / "app" / "routers" / "items.py", items_router)

    # Requirements
    requirements = ["fastapi", "uvicorn[standard]", "pydantic-settings"]
    if include_db:
        requirements.extend(["sqlalchemy", "psycopg2-binary"])
    if include_auth:
        requirements.extend(["python-jose[cryptography]", "passlib[bcrypt]"])

    create_file(project_dir / "requirements.txt", "\n".join(requirements))

    # .env
    env_content = f'''
DEBUG=true
{"DATABASE_URL=postgresql://postgres:postgres@localhost:5432/{name}" if include_db else ""}
{"SECRET_KEY=your-secret-key-change-in-production" if include_auth else ""}
'''
    create_file(project_dir / ".env.example", env_content)
    create_file(project_dir / ".env", env_content)

    # .gitignore
    gitignore = '''
__pycache__/
*.py[cod]
.env
.venv/
venv/
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
'''
    create_file(project_dir / ".gitignore", gitignore)

    # Docker files
    if include_docker:
        dockerfile = f'''
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
        create_file(project_dir / "Dockerfile", dockerfile)

        compose_content = f'''
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=true
      {"- DATABASE_URL=postgresql://postgres:postgres@db:5432/" + name if include_db else ""}
      {"- SECRET_KEY=docker-secret-key" if include_auth else ""}
    {"depends_on:" if include_db else ""}
    {"  - db" if include_db else ""}

{"  db:" if include_db else ""}
{"    image: postgres:16-alpine" if include_db else ""}
{"    environment:" if include_db else ""}
{"      - POSTGRES_USER=postgres" if include_db else ""}
{"      - POSTGRES_PASSWORD=postgres" if include_db else ""}
{"      - POSTGRES_DB=" + name if include_db else ""}
{"    volumes:" if include_db else ""}
{"      - postgres_data:/var/lib/postgresql/data" if include_db else ""}
{"    ports:" if include_db else ""}
{"      - \"5432:5432\"" if include_db else ""}

{"volumes:" if include_db else ""}
{"  postgres_data:" if include_db else ""}
'''
        create_file(project_dir / "docker-compose.yml", compose_content)

    # Tests
    conftest = '''
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)
'''
    create_file(project_dir / "tests" / "conftest.py", conftest)
    create_file(project_dir / "tests" / "__init__.py", "")

    test_main = '''
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
'''
    create_file(project_dir / "tests" / "test_main.py", test_main)

    print(f"\n✅ Project '{name}' created successfully!")
    print(f"\nNext steps:")
    print(f"  cd {project_dir}")
    print(f"  python -m venv venv")
    print(f"  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print(f"  pip install -r requirements.txt")
    print(f"  uvicorn app.main:app --reload")
    print(f"\nAPI docs: http://localhost:8000/docs")

def main():
    parser = argparse.ArgumentParser(description="Scaffold a FastAPI project")
    parser.add_argument("name", help="Project name")
    parser.add_argument("--path", default=".", help="Output directory")
    parser.add_argument("--auth", action="store_true", help="Include JWT auth")
    parser.add_argument("--db", action="store_true", help="Include PostgreSQL")
    parser.add_argument("--docker", action="store_true", help="Include Docker")
    parser.add_argument("--full", action="store_true", help="Include all features")

    args = parser.parse_args()

    include_auth = args.auth or args.full
    include_db = args.db or args.full
    include_docker = args.docker or args.full

    scaffold_project(
        args.name,
        Path(args.path).resolve(),
        include_auth,
        include_db,
        include_docker,
    )

if __name__ == "__main__":
    main()
