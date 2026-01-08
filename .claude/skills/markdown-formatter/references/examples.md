# Markdown Examples

Practical examples of well-formatted markdown for common use cases.

## Table of Contents

1. [README Files](#readme-files)
2. [Technical Documentation](#technical-documentation)
3. [API Documentation](#api-documentation)
4. [Tutorial Content](#tutorial-content)
5. [Blog Posts](#blog-posts)
6. [Meeting Notes](#meeting-notes)

## README Files

### Project README Template

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Installation

```bash
npm install project-name
```

## Quick Start

```javascript
const project = require('project-name');

project.doSomething();
```

## Usage

Detailed usage instructions with examples.

### Basic Example

```javascript
// Example code here
```

### Advanced Example

```javascript
// More complex example
```

## API Reference

See [API Documentation](./docs/API.md) for complete reference.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT License - see [LICENSE](./LICENSE) for details.
```

## Technical Documentation

### Architecture Document

```markdown
# System Architecture

## Overview

High-level description of the system architecture.

## Components

### Frontend

The frontend is built with React and provides:

- User interface
- Client-side routing
- State management

**Technology Stack:**

- React 18
- TypeScript
- Redux Toolkit

### Backend

The backend provides RESTful APIs using:

- Node.js
- Express
- PostgreSQL

### Database Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Data Flow

1. User initiates request from frontend
2. Frontend sends HTTP request to backend API
3. Backend processes request and queries database
4. Backend returns JSON response
5. Frontend updates UI based on response

## Security Considerations

- Authentication via JWT tokens
- HTTPS for all communications
- Input validation and sanitization
- Rate limiting on API endpoints

## Deployment

See [Deployment Guide](./DEPLOYMENT.md) for detailed instructions.
```

## API Documentation

### REST API Example

```markdown
# API Documentation

Base URL: `https://api.example.com/v1`

## Authentication

All API requests require authentication via Bearer token:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/v1/users
```

## Endpoints

### Get User

Retrieve user information by ID.

**Endpoint:** `GET /users/{id}`

**Parameters:**

| Name | Type   | Required | Description           |
|------|--------|----------|-----------------------|
| id   | string | Yes      | The user's unique ID  |

**Response:**

```json
{
  "id": "123",
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Status Codes:**

- `200 OK` - Success
- `404 Not Found` - User not found
- `401 Unauthorized` - Invalid or missing token

**Example:**

```bash
curl -X GET https://api.example.com/v1/users/123 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create User

Create a new user account.

**Endpoint:** `POST /users`

**Request Body:**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Response:**

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
```

## Tutorial Content

### Step-by-Step Tutorial

```markdown
# Getting Started with React Hooks

Learn how to use React Hooks in your applications.

## Prerequisites

Before starting, ensure you have:

- Node.js 16 or higher
- Basic understanding of React
- Text editor (VS Code recommended)

## Step 1: Create a New Project

First, create a new React project:

```bash
npx create-react-app my-app
cd my-app
```

## Step 2: Create Your First Hook

Create a new file `src/useCounter.js`:

```javascript
import { useState } from 'react';

function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount(count + 1);
  const decrement = () => setCount(count - 1);
  const reset = () => setCount(initialValue);

  return { count, increment, decrement, reset };
}

export default useCounter;
```

## Step 3: Use the Hook in a Component

Update `src/App.js`:

```javascript
import useCounter from './useCounter';

function App() {
  const { count, increment, decrement, reset } = useCounter(0);

  return (
    <div>
      <h1>Count: {count}</h1>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}

export default App;
```

## Step 4: Test Your Application

Run the development server:

```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000) to see your app.

## Next Steps

- Learn about `useEffect` hook
- Explore custom hooks patterns
- Read the [React Hooks documentation](https://react.dev/reference/react)

## Troubleshooting

### Common Issues

**Issue:** "Invalid hook call"

**Solution:** Ensure hooks are called at the top level of your component, not inside loops or conditions.

**Issue:** "Too many re-renders"

**Solution:** Check your `useEffect` dependencies to prevent infinite loops.
```

## Blog Posts

### Technical Blog Post

```markdown
# Understanding JavaScript Closures

*Published: January 15, 2024 | Reading time: 5 minutes*

Closures are a fundamental concept in JavaScript that every developer should understand. In this post, we'll explore what closures are and how to use them effectively.

## What is a Closure?

A closure is a function that has access to variables in its outer (enclosing) scope, even after the outer function has returned.

Here's a simple example:

```javascript
function createGreeter(name) {
  return function() {
    console.log(`Hello, ${name}!`);
  };
}

const greetJohn = createGreeter('John');
greetJohn(); // Output: "Hello, John!"
```

## Why Closures Matter

Closures enable several powerful patterns:

1. **Data Privacy** - Create private variables
2. **Factory Functions** - Generate customized functions
3. **Event Handlers** - Maintain state in callbacks
4. **Memoization** - Cache expensive computations

### Example: Data Privacy

```javascript
function createCounter() {
  let count = 0; // Private variable

  return {
    increment() {
      count++;
      return count;
    },
    decrement() {
      count--;
      return count;
    },
    getCount() {
      return count;
    }
  };
}

const counter = createCounter();
console.log(counter.increment()); // 1
console.log(counter.increment()); // 2
console.log(counter.count); // undefined - count is private!
```

## Common Pitfalls

### Pitfall 1: Closures in Loops

A classic gotcha with closures is using them in loops:

```javascript
// Wrong
for (var i = 0; i < 3; i++) {
  setTimeout(function() {
    console.log(i); // Prints "3" three times
  }, 100);
}

// Correct
for (let i = 0; i < 3; i++) {
  setTimeout(function() {
    console.log(i); // Prints 0, 1, 2
  }, 100);
}
```

## Best Practices

- Use closures when you need data privacy
- Be mindful of memory usage with large closures
- Use `let` instead of `var` in loops
- Consider arrow functions for cleaner syntax

## Conclusion

Closures are a powerful feature that enables elegant solutions to common problems. Understanding closures will make you a better JavaScript developer.

## Further Reading

- [MDN: Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)
- [You Don't Know JS: Scope & Closures](https://github.com/getify/You-Dont-Know-JS)

---

*Tags: JavaScript, Closures, Functions, Scope*
```

## Meeting Notes

### Meeting Notes Template

```markdown
# Team Sync Meeting

**Date:** January 15, 2024
**Time:** 10:00 AM - 11:00 AM
**Attendees:** Alice, Bob, Charlie
**Facilitator:** Alice

## Agenda

1. Project status updates
2. Upcoming sprint planning
3. Technical blockers
4. Action items review

## Discussion

### Project Status Updates

**Frontend Team (Alice):**

- Completed user authentication flow
- Working on dashboard UI
- On track for end-of-sprint delivery

**Backend Team (Bob):**

- API endpoints complete
- Database migrations deployed
- Need to discuss rate limiting strategy

**DevOps (Charlie):**

- CI/CD pipeline operational
- Staging environment ready
- Production deployment scheduled for Friday

### Technical Blockers

**Blocker:** API rate limiting not yet implemented

- **Owner:** Bob
- **Impact:** High
- **Resolution:** Implement rate limiting by Wednesday

**Blocker:** Staging database performance issues

- **Owner:** Charlie
- **Impact:** Medium
- **Resolution:** Increase database resources

## Decisions Made

1. Deploy to production on Friday at 5 PM
2. Use Redis for rate limiting implementation
3. Schedule performance review meeting for next week

## Action Items

- [ ] Bob: Implement API rate limiting by Jan 17
- [ ] Charlie: Upgrade staging database by Jan 16
- [ ] Alice: Review dashboard designs with design team
- [ ] All: Prepare sprint retrospective notes

## Next Meeting

**Date:** January 22, 2024
**Time:** 10:00 AM
**Agenda:** Sprint retrospective and planning
```

## Quick Reference: Common Elements

### Callouts and Alerts

```markdown
> **Note:** This is important information.

> **Warning:** Be careful with this operation.

> **Tip:** Here's a helpful suggestion.
```

### Task Lists

```markdown
## TODO

- [x] Completed task
- [ ] Pending task
- [ ] Another pending task
```

### Definition Lists

```markdown
**Term**
: Definition of the term

**Another Term**
: Definition of another term
```

### Footnotes

```markdown
Here is some text with a footnote.[^1]

[^1]: This is the footnote content.
```

### Abbreviations

```markdown
The HTML specification is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium
```
