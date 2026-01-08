# Routing Reference

## Table of Contents
- [Basic Routes](#basic-routes)
- [Path Parameters](#path-parameters)
- [Query Parameters](#query-parameters)
- [Request Body](#request-body)
- [Response Models](#response-models)
- [APIRouter](#apirouter)
- [Dependencies](#dependencies)

---

## Basic Routes

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/items/")
def create_item():
    return {"action": "created"}

@app.put("/items/{item_id}")
def update_item(item_id: int):
    return {"item_id": item_id, "action": "updated"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"item_id": item_id, "action": "deleted"}

@app.patch("/items/{item_id}")
def patch_item(item_id: int):
    return {"item_id": item_id, "action": "patched"}
```

---

## Path Parameters

```python
from fastapi import FastAPI, Path
from enum import Enum

app = FastAPI()

# Basic path parameter with type validation
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

# Multiple path parameters
@app.get("/users/{user_id}/items/{item_id}")
def get_user_item(user_id: int, item_id: int):
    return {"user_id": user_id, "item_id": item_id}

# Path parameter with validation
@app.get("/items/{item_id}/validated")
def get_validated_item(
    item_id: int = Path(..., gt=0, le=1000, description="Item ID between 1-1000")
):
    return {"item_id": item_id}

# Enum path parameter
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    return {"model": model_name, "message": f"Selected {model_name.value}"}

# File path parameter (captures slashes)
@app.get("/files/{file_path:path}")
def get_file(file_path: str):
    return {"file_path": file_path}
```

---

## Query Parameters

```python
from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

# Basic query parameters
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# Optional query parameter
@app.get("/items/search")
def search_items(q: str | None = None):
    return {"query": q}

# Required query parameter
@app.get("/items/required")
def required_query(q: str):
    return {"query": q}

# Query with validation
@app.get("/items/validated")
def validated_query(
    q: Annotated[str, Query(min_length=3, max_length=50)] = None,
    page: Annotated[int, Query(ge=1, le=100)] = 1,
):
    return {"query": q, "page": page}

# List query parameters (?tags=a&tags=b)
@app.get("/items/tags")
def items_with_tags(tags: list[str] = Query(default=[])):
    return {"tags": tags}

# Alias for query parameter
@app.get("/items/alias")
def aliased_query(item_query: str = Query(alias="item-query")):
    return {"query": item_query}
```

---

## Request Body

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

# Basic request body
@app.post("/items/")
def create_item(item: Item):
    return item

# Body with path/query params
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, q: str | None = None):
    return {"item_id": item_id, **item.model_dump(), "q": q}

# Multiple body parameters
class User(BaseModel):
    username: str
    email: str

@app.post("/items/with-user/")
def create_with_user(item: Item, user: User):
    return {"item": item, "user": user}

# Embed single body in key
@app.post("/items/embedded/")
def embedded_body(item: Annotated[Item, Body(embed=True)]):
    # Expects: {"item": {"name": "...", "price": ...}}
    return item

# Singular body values
@app.post("/items/importance/")
def with_importance(
    item: Item,
    importance: Annotated[int, Body(gt=0)]
):
    return {"item": item, "importance": importance}
```

---

## Response Models

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ItemCreate(BaseModel):
    name: str
    price: float
    description: str | None = None

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None

    model_config = {"from_attributes": True}

# Response model filters output
@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate):
    # Even if we return extra fields, only ItemResponse fields are sent
    return {"id": 1, **item.model_dump(), "internal_code": "secret"}

# Multiple response models
class ItemPublic(BaseModel):
    name: str
    price: float

class ItemAdmin(BaseModel):
    id: int
    name: str
    price: float
    internal_code: str

@app.get("/items/{item_id}/public", response_model=ItemPublic)
def get_public(item_id: int):
    return {"name": "Item", "price": 9.99, "internal_code": "X123"}

@app.get("/items/{item_id}/admin", response_model=ItemAdmin)
def get_admin(item_id: int):
    return {"id": item_id, "name": "Item", "price": 9.99, "internal_code": "X123"}

# List response
@app.get("/items/", response_model=list[ItemResponse])
def list_items():
    return [{"id": 1, "name": "Item 1", "price": 9.99}]

# Exclude unset fields
@app.get("/items/{item_id}/sparse", response_model=ItemResponse, response_model_exclude_unset=True)
def get_sparse(item_id: int):
    return {"id": item_id, "name": "Item"}  # description not included in response
```

---

## APIRouter

Organize routes into modules:

```python
# app/routers/items.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def list_items():
    return []

@router.get("/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

@router.post("/")
def create_item():
    return {"created": True}
```

```python
# app/routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users():
    return []

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

```python
# app/main.py
from fastapi import FastAPI
from app.routers import items, users

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)
# Routes: /items/, /items/{id}, /users/, /users/{id}
```

---

## Dependencies

```python
from fastapi import FastAPI, Depends, Query, Header, HTTPException
from typing import Annotated

app = FastAPI()

# Simple dependency
def common_parameters(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}

@app.get("/items/")
def list_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

# Class-based dependency
class Pagination:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/users/")
def list_users(pagination: Annotated[Pagination, Depends()]):
    return {"skip": pagination.skip, "limit": pagination.limit}

# Dependency with validation
def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "secret-token":
        raise HTTPException(status_code=403, detail="Invalid token")
    return x_token

@app.get("/protected/", dependencies=[Depends(verify_token)])
def protected_route():
    return {"message": "Access granted"}

# Nested dependencies
def get_db():
    return {"db": "connection"}

def get_current_user(db=Depends(get_db)):
    return {"user": "john", "db": db}

@app.get("/me/")
def get_me(user=Depends(get_current_user)):
    return user

# Yield dependencies (cleanup)
def get_db_session():
    db = {"session": "active"}
    try:
        yield db
    finally:
        print("Closing DB session")

@app.get("/db/")
def use_db(db=Depends(get_db_session)):
    return db
```
