# Pydantic Models Reference

## Table of Contents
- [Basic Models](#basic-models)
- [Field Validation](#field-validation)
- [Nested Models](#nested-models)
- [Model Inheritance](#model-inheritance)
- [Custom Validators](#custom-validators)
- [Model Config](#model-config)
- [Common Patterns](#common-patterns)

---

## Basic Models

```python
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool = True  # Default value
    created_at: datetime | None = None  # Optional field

# Usage
user = User(id=1, username="john", email="john@example.com")
print(user.model_dump())  # Convert to dict
print(user.model_dump_json())  # Convert to JSON string
```

---

## Field Validation

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

class User(BaseModel):
    # String validation
    username: str = Field(min_length=3, max_length=50)

    # Email validation (requires: pip install pydantic[email])
    email: EmailStr

    # Numeric validation
    age: int = Field(ge=0, le=150)  # 0 <= age <= 150
    score: float = Field(gt=0, lt=100)  # 0 < score < 100

    # Pattern matching
    phone: str = Field(pattern=r"^\+?1?\d{9,15}$")

    # With description (shows in OpenAPI docs)
    bio: str = Field(default="", max_length=500, description="User biography")

class Item(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    price: Annotated[float, Field(gt=0, description="Price must be positive")]
    quantity: Annotated[int, Field(ge=0, default=0)]

class Config(BaseModel):
    # List with constraints
    tags: list[str] = Field(default_factory=list, max_length=10)

    # Dict validation
    metadata: dict[str, str] = Field(default_factory=dict)

    # Literal values
    from typing import Literal
    status: Literal["draft", "published", "archived"] = "draft"
```

---

## Nested Models

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str | None = None

class Company(BaseModel):
    name: str
    address: Address

class User(BaseModel):
    username: str
    email: str
    address: Address | None = None
    company: Company | None = None

# Usage in FastAPI
from fastapi import FastAPI
app = FastAPI()

@app.post("/users/")
def create_user(user: User):
    return user

# Request body:
# {
#   "username": "john",
#   "email": "john@example.com",
#   "address": {
#     "street": "123 Main St",
#     "city": "NYC",
#     "country": "USA"
#   }
# }

# Lists of nested models
class Order(BaseModel):
    id: int
    items: list[Item]

class Item(BaseModel):
    name: str
    quantity: int
    price: float
```

---

## Model Inheritance

```python
from pydantic import BaseModel
from datetime import datetime

# Base model with common fields
class TimestampMixin(BaseModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None

# Create/Update/Response pattern
class UserBase(BaseModel):
    username: str
    email: str
    full_name: str | None = None

class UserCreate(UserBase):
    password: str  # Only for creation

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    password: str | None = None

class UserInDB(UserBase, TimestampMixin):
    id: int
    hashed_password: str

    model_config = {"from_attributes": True}

class UserResponse(UserBase, TimestampMixin):
    id: int
    # password/hashed_password excluded from response

# Usage
from fastapi import FastAPI
app = FastAPI()

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    # UserCreate has password
    # UserResponse excludes password
    db_user = {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": "hashed_" + user.password,
        "created_at": datetime.now(),
    }
    return db_user
```

---

## Custom Validators

```python
from pydantic import BaseModel, field_validator, model_validator
from typing import Self

class User(BaseModel):
    username: str
    email: str
    password: str
    password_confirm: str

    # Field validator
    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.lower()  # Transform value

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email")
        return v.lower()

    # Model validator (access multiple fields)
    @model_validator(mode="after")
    def passwords_match(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self

class Item(BaseModel):
    name: str
    price: float
    discount_price: float | None = None

    @model_validator(mode="after")
    def discount_less_than_price(self) -> Self:
        if self.discount_price and self.discount_price >= self.price:
            raise ValueError("Discount price must be less than price")
        return self

# Before validator (runs before Pydantic validation)
class Product(BaseModel):
    tags: list[str]

    @field_validator("tags", mode="before")
    @classmethod
    def split_tags(cls, v):
        if isinstance(v, str):
            return v.split(",")
        return v

# Usage: Product(tags="a,b,c") -> Product(tags=["a", "b", "c"])
```

---

## Model Config

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        # Allow creating from ORM objects
        from_attributes=True,

        # Strip whitespace from strings
        str_strip_whitespace=True,

        # Validate default values
        validate_default=True,

        # Extra fields handling
        extra="forbid",  # "allow", "ignore", or "forbid"

        # JSON schema customization
        json_schema_extra={
            "examples": [
                {"username": "john", "email": "john@example.com"}
            ]
        },
    )

    username: str
    email: str

# From ORM/database objects
class UserORM:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str

# Convert ORM to Pydantic
orm_user = UserORM(1, "john", "john@example.com")
pydantic_user = UserSchema.model_validate(orm_user)
```

---

## Common Patterns

### Request/Response Models

```python
from pydantic import BaseModel
from datetime import datetime

# Input models
class ItemCreate(BaseModel):
    name: str
    price: float
    description: str | None = None

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None

# Output models
class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}

# Paginated response
class PaginatedResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    per_page: int
    pages: int
```

### Generic Response Wrapper

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    message: str | None = None
    errors: list[str] | None = None

# Usage
@app.get("/items/{id}", response_model=APIResponse[ItemResponse])
def get_item(id: int):
    return APIResponse(
        success=True,
        data={"id": id, "name": "Item", "price": 9.99},
    )
```

### Enum Fields

```python
from pydantic import BaseModel
from enum import Enum

class Status(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Priority(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task(BaseModel):
    title: str
    status: Status = Status.PENDING
    priority: Priority = Priority.MEDIUM
```
