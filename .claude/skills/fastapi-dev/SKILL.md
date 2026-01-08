---
name: fastapi-dev
description: Build FastAPI applications from hello world to production-ready. Use when creating new FastAPI projects, implementing REST APIs, adding authentication (JWT), database integration (PostgreSQL/SQLAlchemy), middleware, testing, or Docker deployment. Includes scaffolding script and comprehensive reference patterns.
---

# FastAPI Development

Build production-ready FastAPI applications with best practices.

## Quick Start

### New Project
```bash
# Scaffold a complete project
python scripts/scaffold.py myapp --full

# Or with specific features
python scripts/scaffold.py myapp --auth --db --docker
```

### Hello World
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

# Run: uvicorn main:app --reload
# Docs: http://localhost:8000/docs
```

---

## Core Patterns

### Project Structure
```
project/
├── app/
│   ├── main.py           # FastAPI app, middleware, routers
│   ├── core/
│   │   ├── config.py     # Settings with pydantic-settings
│   │   ├── database.py   # SQLAlchemy setup
│   │   ├── security.py   # Password hashing, JWT
│   │   └── deps.py       # Dependencies (get_db, get_current_user)
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic models
│   ├── crud/             # Database operations
│   └── routers/          # API endpoints
├── tests/
├── alembic/              # Migrations
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

### Basic CRUD Router
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.schemas.item import ItemCreate, ItemResponse
from app.crud import item as item_crud

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=list[ItemResponse])
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return item_crud.get_items(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = item_crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return item_crud.create_item(db, item)
```

### Pydantic Schema Pattern
```python
from pydantic import BaseModel, Field
from datetime import datetime

class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None

class ItemResponse(ItemBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
```

### Protected Route
```python
from fastapi import Depends
from typing import Annotated
from app.core.deps import get_current_user

@router.get("/me")
def get_me(current_user: Annotated[dict, Depends(get_current_user)]):
    return current_user
```

---

## Reference Documentation

Detailed patterns and examples for specific features:

| Topic | Reference | Use When |
|-------|-----------|----------|
| **Routing** | [routing.md](references/routing.md) | Path/query params, response models, APIRouter, dependencies |
| **Models** | [models.md](references/models.md) | Pydantic validation, nested models, custom validators |
| **Auth** | [auth.md](references/auth.md) | JWT tokens, login/register, protected routes, RBAC |
| **Database** | [database.md](references/database.md) | SQLAlchemy models, CRUD, async, migrations, relationships |
| **Middleware** | [middleware.md](references/middleware.md) | CORS, custom middleware, exception handlers, background tasks |
| **Testing** | [testing.md](references/testing.md) | pytest, TestClient, fixtures, database testing, async tests |
| **Deployment** | [deployment.md](references/deployment.md) | Docker, docker-compose, production settings, health checks |

---

## Common Tasks

### Add CORS
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Database Dependency
```python
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### JWT Auth Dependency
```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user_id": payload.get("sub")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Error Response
```python
from fastapi import HTTPException

# 404
raise HTTPException(status_code=404, detail="Item not found")

# 400 with extra info
raise HTTPException(status_code=400, detail={"error": "Invalid data", "field": "email"})

# 401 with auth header
raise HTTPException(
    status_code=401,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
```

### Background Task
```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email logic
    pass

@app.post("/notify/{email}")
async def notify(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, "Hello!")
    return {"message": "Notification scheduled"}
```

---

## Dependencies

### Base
```
fastapi
uvicorn[standard]
pydantic-settings
```

### With Database
```
sqlalchemy
psycopg2-binary
alembic
```

### With Auth
```
python-jose[cryptography]
passlib[bcrypt]
```

### Testing
```
pytest
pytest-asyncio
httpx
```
