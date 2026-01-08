# Testing Reference

## Table of Contents
- [Setup](#setup)
- [Basic Testing](#basic-testing)
- [Testing with Database](#testing-with-database)
- [Testing Authentication](#testing-authentication)
- [Async Testing](#async-testing)
- [Fixtures and Factories](#fixtures-and-factories)
- [Coverage](#coverage)

---

## Setup

Install dependencies:
```bash
pip install pytest pytest-asyncio httpx
```

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
asyncio_mode = auto
```

```
# Project structure
project/
├── app/
│   ├── main.py
│   └── routers/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_main.py
│   └── test_users.py
```

---

## Basic Testing

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)
```

```python
# tests/test_main.py
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_get_item(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["item_id"] == 1

def test_create_item(client):
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 9.99},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_create_item_invalid(client):
    response = client.post(
        "/items/",
        json={"name": "Test"},  # Missing required 'price'
    )
    assert response.status_code == 422

def test_not_found(client):
    response = client.get("/items/99999")
    assert response.status_code == 404

def test_query_params(client):
    response = client.get("/items/", params={"skip": 0, "limit": 10})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

---

## Testing with Database

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

```python
# tests/test_users.py
def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_duplicate_user(client):
    # Create first user
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "pass"},
    )
    # Try duplicate
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test2@example.com", "password": "pass"},
    )
    assert response.status_code == 400

def test_get_user(client, db):
    # Create user directly in db
    from app.models.user import User
    from app.core.security import get_password_hash

    user = User(
        username="dbuser",
        email="db@example.com",
        hashed_password=get_password_hash("password"),
    )
    db.add(user)
    db.commit()

    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["username"] == "dbuser"
```

---

## Testing Authentication

```python
# tests/conftest.py
from app.core.security import create_access_token

@pytest.fixture
def auth_headers():
    token = create_access_token(data={"sub": 1, "username": "testuser"})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers():
    token = create_access_token(data={"sub": 1, "username": "admin", "role": "admin"})
    return {"Authorization": f"Bearer {token}"}
```

```python
# tests/test_auth.py
def test_login(client, db):
    # Create user first
    from app.models.user import User
    from app.core.security import get_password_hash

    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass"),
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpass"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid(client):
    response = client.post(
        "/auth/login",
        data={"username": "wrong", "password": "wrong"},
    )
    assert response.status_code == 401

def test_protected_route(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200

def test_protected_route_no_auth(client):
    response = client.get("/users/me")
    assert response.status_code == 401

def test_admin_only_route(client, auth_headers, admin_headers):
    # Regular user denied
    response = client.delete("/admin/users/1", headers=auth_headers)
    assert response.status_code == 403

    # Admin allowed
    response = client.delete("/admin/users/1", headers=admin_headers)
    assert response.status_code in [200, 404]
```

---

## Async Testing

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.core.database import Base, get_db

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
AsyncTestingSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture
async def async_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncTestingSession() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def async_client(async_db):
    async def override_get_db():
        yield async_db

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
```

```python
# tests/test_async.py
import pytest

@pytest.mark.asyncio
async def test_async_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_async_create_item(async_client):
    response = await async_client.post(
        "/items/",
        json={"name": "Async Item", "price": 19.99},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Async Item"
```

---

## Fixtures and Factories

```python
# tests/factories.py
from app.models.user import User
from app.models.post import Post
from app.core.security import get_password_hash

class UserFactory:
    @staticmethod
    def create(db, **kwargs):
        defaults = {
            "username": "testuser",
            "email": "test@example.com",
            "hashed_password": get_password_hash("password"),
            "is_active": True,
        }
        defaults.update(kwargs)
        user = User(**defaults)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

class PostFactory:
    @staticmethod
    def create(db, author_id: int, **kwargs):
        defaults = {
            "title": "Test Post",
            "content": "Test content",
            "author_id": author_id,
        }
        defaults.update(kwargs)
        post = Post(**defaults)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
```

```python
# tests/conftest.py
from tests.factories import UserFactory, PostFactory

@pytest.fixture
def user(db):
    return UserFactory.create(db)

@pytest.fixture
def user_with_posts(db):
    user = UserFactory.create(db)
    for i in range(3):
        PostFactory.create(db, author_id=user.id, title=f"Post {i}")
    return user
```

```python
# tests/test_posts.py
def test_get_user_posts(client, user_with_posts, auth_headers):
    response = client.get(f"/users/{user_with_posts.id}/posts", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 3
```

---

## Coverage

```bash
# Install
pip install pytest-cov

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term-missing

# View HTML report
open htmlcov/index.html
```

```ini
# .coveragerc
[run]
source = app
omit =
    app/tests/*
    app/__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
```
