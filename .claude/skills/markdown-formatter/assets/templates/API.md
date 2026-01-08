# API Documentation

**Version:** 1.0
**Base URL:** `https://api.example.com/v1`
**Last Updated:** [Date]

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Rate Limiting](#rate-limiting)
4. [Error Handling](#error-handling)
5. [Endpoints](#endpoints)

## Overview

Brief description of the API and its purpose.

### Key Features

- Feature 1
- Feature 2
- Feature 3

### API Versioning

This API uses URL versioning. The current version is `v1`.

```
https://api.example.com/v1/resource
```

## Authentication

All API requests require authentication via Bearer token in the Authorization header.

### Obtaining a Token

**Endpoint:** `POST /auth/login`

**Request:**

```json
{
  "username": "user@example.com",
  "password": "your_password"
}
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

### Using the Token

Include the token in the Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/v1/users
```

## Rate Limiting

Rate limits are enforced to ensure fair usage:

- **Authenticated requests:** 1000 requests per hour
- **Unauthenticated requests:** 100 requests per hour

### Rate Limit Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1234567890
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional context"
    }
  }
}
```

### HTTP Status Codes

| Code | Description                |
|------|----------------------------|
| 200  | OK - Request succeeded     |
| 201  | Created - Resource created |
| 400  | Bad Request - Invalid input |
| 401  | Unauthorized - Invalid token |
| 403  | Forbidden - Access denied |
| 404  | Not Found - Resource not found |
| 429  | Too Many Requests - Rate limit exceeded |
| 500  | Internal Server Error |

### Common Error Codes

| Code                  | Description                     |
|-----------------------|---------------------------------|
| INVALID_REQUEST       | Request format is invalid       |
| AUTHENTICATION_FAILED | Authentication credentials failed |
| RESOURCE_NOT_FOUND    | Requested resource not found    |
| VALIDATION_ERROR      | Request validation failed       |
| RATE_LIMIT_EXCEEDED   | Rate limit exceeded             |

## Endpoints

### Users

#### List Users

Retrieve a list of users.

**Endpoint:** `GET /users`

**Query Parameters:**

| Name   | Type   | Required | Default | Description           |
|--------|--------|----------|---------|----------------------|
| page   | number | No       | 1       | Page number           |
| limit  | number | No       | 20      | Items per page        |
| sort   | string | No       | id      | Sort field            |
| order  | string | No       | asc     | Sort order (asc/desc) |

**Example Request:**

```bash
curl -X GET "https://api.example.com/v1/users?page=1&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Example Response:**

```json
{
  "data": [
    {
      "id": "123",
      "username": "john_doe",
      "email": "john@example.com",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "pages": 10
  }
}
```

**Status Codes:**

- `200 OK` - Success
- `401 Unauthorized` - Invalid or missing token

#### Get User

Retrieve a specific user by ID.

**Endpoint:** `GET /users/{id}`

**Path Parameters:**

| Name | Type   | Required | Description          |
|------|--------|----------|----------------------|
| id   | string | Yes      | User's unique ID     |

**Example Request:**

```bash
curl -X GET "https://api.example.com/v1/users/123" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Example Response:**

```json
{
  "id": "123",
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Status Codes:**

- `200 OK` - Success
- `404 Not Found` - User not found
- `401 Unauthorized` - Invalid or missing token

#### Create User

Create a new user.

**Endpoint:** `POST /users`

**Request Body:**

| Field    | Type   | Required | Description           |
|----------|--------|----------|-----------------------|
| username | string | Yes      | Unique username       |
| email    | string | Yes      | Valid email address   |
| password | string | Yes      | Password (min 8 chars) |

**Example Request:**

```bash
curl -X POST "https://api.example.com/v1/users" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password"
  }'
```

**Example Response:**

```json
{
  "id": "123",
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Status Codes:**

- `201 Created` - User created successfully
- `400 Bad Request` - Invalid input
- `409 Conflict` - Username or email already exists
- `401 Unauthorized` - Invalid or missing token

#### Update User

Update an existing user.

**Endpoint:** `PUT /users/{id}`

**Path Parameters:**

| Name | Type   | Required | Description      |
|------|--------|----------|------------------|
| id   | string | Yes      | User's unique ID |

**Request Body:**

| Field    | Type   | Required | Description         |
|----------|--------|----------|---------------------|
| username | string | No       | New username        |
| email    | string | No       | New email address   |

**Example Request:**

```bash
curl -X PUT "https://api.example.com/v1/users/123" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com"
  }'
```

**Example Response:**

```json
{
  "id": "123",
  "username": "john_doe",
  "email": "newemail@example.com",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**Status Codes:**

- `200 OK` - User updated successfully
- `400 Bad Request` - Invalid input
- `404 Not Found` - User not found
- `401 Unauthorized` - Invalid or missing token

#### Delete User

Delete a user.

**Endpoint:** `DELETE /users/{id}`

**Path Parameters:**

| Name | Type   | Required | Description      |
|------|--------|----------|------------------|
| id   | string | Yes      | User's unique ID |

**Example Request:**

```bash
curl -X DELETE "https://api.example.com/v1/users/123" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Example Response:**

```json
{
  "message": "User deleted successfully"
}
```

**Status Codes:**

- `200 OK` - User deleted successfully
- `404 Not Found` - User not found
- `401 Unauthorized` - Invalid or missing token

## Webhooks

Configure webhooks to receive real-time notifications.

### Webhook Events

| Event        | Description                 |
|--------------|-----------------------------|
| user.created | Triggered when user created |
| user.updated | Triggered when user updated |
| user.deleted | Triggered when user deleted |

### Webhook Payload

```json
{
  "event": "user.created",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "id": "123",
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

## SDKs and Libraries

Official client libraries:

- **JavaScript/Node.js:** [npm package](https://www.npmjs.com/package/api-client)
- **Python:** [pip package](https://pypi.org/project/api-client/)
- **Ruby:** [gem](https://rubygems.org/gems/api-client)

## Support

- **Documentation:** [https://docs.example.com](https://docs.example.com)
- **API Status:** [https://status.example.com](https://status.example.com)
- **Support Email:** support@example.com
- **GitHub Issues:** [https://github.com/example/api/issues](https://github.com/example/api/issues)

## Changelog

### v1.0.0 (2024-01-15)

- Initial API release
- User management endpoints
- Authentication with JWT tokens
