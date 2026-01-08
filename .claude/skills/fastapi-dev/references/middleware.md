# Middleware Reference

## Table of Contents
- [Built-in Middleware](#built-in-middleware)
- [Custom Middleware](#custom-middleware)
- [Exception Handlers](#exception-handlers)
- [Background Tasks](#background-tasks)
- [Lifespan Events](#lifespan-events)

---

## Built-in Middleware

### CORS Middleware
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://myapp.com"],  # Or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],  # Or specific: ["GET", "POST"]
    allow_headers=["*"],
)
```

### Trusted Host Middleware
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"],
)
```

### GZip Middleware
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)  # Compress responses > 1KB
```

### HTTPS Redirect
```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
```

---

## Custom Middleware

### Function-based Middleware
```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Class-based Middleware
```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response

app.add_middleware(LoggingMiddleware)
```

### Request ID Middleware
```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

# Access in route
@app.get("/")
def root(request: Request):
    return {"request_id": request.state.request_id}
```

### Authentication Middleware
```python
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_paths: list[str] = None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or ["/docs", "/openapi.json", "/health"]

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.excluded_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(status_code=401, content="Unauthorized")

        return await call_next(request)

app.add_middleware(AuthMiddleware, excluded_paths=["/docs", "/health", "/auth/login"])
```

### Rate Limiting Middleware
```python
from collections import defaultdict
from datetime import datetime, timedelta
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)

        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > minute_ago
        ]

        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"},
            )

        self.requests[client_ip].append(now)
        return await call_next(request)
```

---

## Exception Handlers

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

app = FastAPI()

# Custom exception
class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

# Handler for custom exception
@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Item {exc.item_id} not found"},
    )

# Handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "path": str(request.url),
        },
    )

# Handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
        },
    )

# Catch-all handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Usage
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id > 100:
        raise ItemNotFoundError(item_id)
    return {"item_id": item_id}
```

---

## Background Tasks

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def send_email(email: str, message: str):
    # Simulate sending email
    import time
    time.sleep(2)
    print(f"Email sent to {email}: {message}")

def log_operation(operation: str, user_id: int):
    print(f"User {user_id} performed: {operation}")

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification scheduled"}

# Multiple background tasks
@app.post("/users/{user_id}/action")
async def user_action(
    user_id: int,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(log_operation, "action", user_id)
    background_tasks.add_task(send_email, f"user{user_id}@example.com", "Action completed")
    return {"status": "ok"}

# Background task in dependency
def get_background_task_dep(background_tasks: BackgroundTasks):
    def log_after():
        background_tasks.add_task(print, "Request completed")
    return log_after
```

---

## Lifespan Events

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Resources to initialize/cleanup
db_connection = None
cache = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global db_connection
    print("Starting up...")
    db_connection = await create_db_connection()
    cache["config"] = await load_config()

    yield  # App runs here

    # Shutdown
    print("Shutting down...")
    await db_connection.close()
    cache.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"db": "connected" if db_connection else "disconnected"}
```

### Alternative: Event Handlers (deprecated but still works)
```python
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
```
