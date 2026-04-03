# Level 5: Team Task Board

**Time Budget:** ~6-8 hours  
**Difficulty:** Very High  
**Focus:** Full-stack, real-time, authentication, database migrations, Docker Compose, CI

## Problem Statement

Build a complete team task management application with a REST API backend, real-time updates, user authentication, and a functional web frontend. The entire system must start with a single `docker-compose up` command.

## Requirements

### Backend: REST API + WebSocket

**Authentication**:
- JWT-based authentication (register, login, refresh)
- Protected endpoints require valid token
- Role-based access: admin and member roles

**Task Management**:
```
POST   /api/tasks                 # Create task
GET    /api/tasks                 # List tasks (with filters: status, assignee, board)
GET    /api/tasks/{id}            # Get task details
PUT    /api/tasks/{id}            # Update task
DELETE /api/tasks/{id}            # Delete task (admin only)
PATCH  /api/tasks/{id}/move       # Move task to different column/status
```

**Kanban Boards**:
```
POST   /api/boards                # Create board
GET    /api/boards                # List boards
GET    /api/boards/{id}           # Get board with all columns and tasks
PUT    /api/boards/{id}           # Update board
DELETE /api/boards/{id}           # Delete board (admin only)

POST   /api/boards/{id}/columns   # Add column to board
PUT    /api/columns/{id}          # Update column (name, position)
DELETE /api/columns/{id}          # Delete column
```

**Activity Log**:
```
GET    /api/activity               # Recent activity across all boards
GET    /api/boards/{id}/activity   # Activity for a specific board
```

Every task mutation (create, update, move, delete) should create an activity log entry.

**Real-Time (WebSocket)**:
- WebSocket endpoint at `/ws`
- Broadcast task updates to all connected clients on a board
- Events: `task.created`, `task.updated`, `task.moved`, `task.deleted`
- Clients subscribe to specific board channels

**Users**:
```
POST   /api/auth/register          # Register new user
POST   /api/auth/login             # Login, receive JWT
POST   /api/auth/refresh           # Refresh token
GET    /api/users/me               # Current user profile
GET    /api/users                  # List users (admin only)
```

### Database

- PostgreSQL (via Docker)
- Database migrations (Alembic, Django migrations, or similar)
- Seed data script: creates default admin user, sample board with columns, sample tasks

### Frontend

Build a web interface using one of:
- **Server-rendered HTML with HTMX** (preferred for simplicity)
- **React SPA** (if agent prefers)
- **Other** (Svelte, Vue, etc.)

The frontend must support:
- Login/register forms
- Board view with columns (Kanban layout)
- Drag-and-drop task movement between columns (or click-based move)
- Real-time updates (tasks appear/move without page refresh)
- Task detail view/modal
- Create/edit task forms
- Activity feed

### Infrastructure

**Docker Compose** must include:
- Application server (Python backend)
- PostgreSQL database
- Frontend (if SPA, served by nginx or built into backend)
- Optional: Redis for WebSocket pub/sub in multi-worker setup

**The following must work**:
```bash
# Start everything
docker-compose up

# Seed the database
docker-compose exec app python manage.py seed
# or
docker-compose exec app python -m task_board seed

# Run tests
docker-compose exec app pytest
```

**CI Configuration**: Include a GitHub Actions workflow (`.github/workflows/ci.yml`) that:
- Runs tests
- Runs linting
- Builds Docker images

### API Documentation

Include OpenAPI/Swagger documentation accessible at `/docs` or `/api/docs`.

## Data Model

```
User:
  - id, email, password_hash, display_name, role (admin/member), created_at

Board:
  - id, name, description, created_by (FK User), created_at

Column:
  - id, board_id (FK Board), name, position (integer for ordering)

Task:
  - id, title, description, column_id (FK Column), assignee_id (FK User, nullable)
  - priority (low/medium/high/urgent), due_date, created_by (FK User)
  - created_at, updated_at

Activity:
  - id, board_id (FK Board), user_id (FK User), task_id (FK Task, nullable)
  - action (created/updated/moved/deleted/commented), details (JSON), created_at
```

## Deliverables

1. Backend application with all API endpoints and WebSocket
2. Frontend with Kanban board UI
3. PostgreSQL with migrations and seed data
4. Docker Compose configuration
5. CI configuration (GitHub Actions)
6. Comprehensive tests (unit, integration, API)
7. API documentation (OpenAPI/Swagger)
8. README with architecture decisions, setup, and usage

## Open Decisions (Agent's Choice)

- Backend framework (FastAPI, Django, Flask)
- Frontend approach (HTMX, React, Svelte, Vue)
- ORM (SQLAlchemy, Django ORM, Tortoise)
- Migration tool (Alembic, Django migrations)
- WebSocket implementation (native, socket.io, channels)
- CSS framework (Tailwind, Bootstrap, custom)
- Session management strategy
- Rate limiting approach
- How to handle WebSocket auth

## Evaluation Criteria

See `evaluation/rubric.md` for the full scoring rubric. Key weights for this level:

- **Correctness**: 15%
- **Code Quality**: 10%
- **Architecture**: 25%
- **Testing**: 15%
- **Error Handling**: 10%
- **Documentation**: 10%
- **Bonus (Real-time, Docker, CI)**: 15%
