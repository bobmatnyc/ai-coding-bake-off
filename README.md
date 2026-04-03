# Team Task Board

A complete team task management application with real-time updates, authentication, and a REST API backend.

## Features

- JWT-based authentication (register, login, refresh)
- Protected endpoints requiring valid token
- Role-based access: admin and member roles
- Task management with CRUD operations
- Kanban boards with columns
- Activity logging for all task mutations
- Real-time WebSocket updates
- PostgreSQL database with migrations
- Docker Compose for easy deployment

## Requirements

- Python 3.12+
- Docker and Docker Compose
- PostgreSQL (via Docker)

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd task-board
   ```

2. Start the application with Docker Compose:
   ```
   docker-compose up
   ```

3. Seed the database:
   ```
   docker-compose exec app python -m task_board seed
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login, receive JWT
- `POST /api/auth/refresh` - Refresh token

### Users
- `GET /api/users/me` - Current user profile
- `GET /api/users` - List users (admin only)

### Boards
- `POST /api/boards` - Create board
- `GET /api/boards` - List boards
- `GET /api/boards/{id}` - Get board with all columns and tasks
- `PUT /api/boards/{id}` - Update board
- `DELETE /api/boards/{id}` - Delete board (admin only)

### Columns
- `POST /api/boards/{id}/columns` - Add column to board
- `PUT /api/columns/{id}` - Update column (name, position)
- `DELETE /api/columns/{id}` - Delete column

### Tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks` - List tasks
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task (admin only)
- `PATCH /api/tasks/{id}/move` - Move task to different column/status

### Activity
- `GET /api/activity` - Recent activity across all boards
- `GET /api/boards/{id}/activity` - Activity for a specific board

## WebSocket

- WebSocket endpoint at `/ws/{board_id}`
- Broadcast task updates to all connected clients on a board
- Events: `task.created`, `task.updated`, `task.moved`, `task.deleted`
- Clients subscribe to specific board channels

## Testing

Run the tests with:
```
docker-compose exec app pytest
```

## Database Migrations

Alembic is used for database migrations. To create a new migration:
```
docker-compose exec app alembic revision --autogenerate -m "Description of changes"
```

To apply migrations:
```
docker-compose exec app alembic upgrade head
```

## Architecture

The application follows a clean architecture pattern with:

1. **FastAPI** for the web framework
2. **SQLAlchemy** for ORM
3. **PostgreSQL** for the database
4. **JWT** for authentication
5. **WebSockets** for real-time updates
6. **Docker Compose** for containerization

## Project Structure

```
task_board/
├── main.py              # Application entry point
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication utilities
├── deps.py              # FastAPI dependencies
├── websocket.py         # WebSocket connection manager
├── routes/              # API route handlers
│   ├── auth.py
│   ├── users.py
│   ├── boards.py
│   ├── tasks.py
│   ├── columns.py
│   └── activity.py
├── seed.py              # Database seeding script
tests/                   # Test suite
Dockerfile               # Docker configuration
docker-compose.yml       # Docker Compose configuration
requirements.txt         # Python dependencies
alembic/                 # Database migrations
.github/workflows/       # CI configuration
```

## Development

To run the application locally without Docker:

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```
   export DATABASE_URL=sqlite:///./test.db
   export SECRET_KEY=your-secret-key
   ```

3. Run the application:
   ```
   uvicorn task_board.main:app --reload
   ```

## License

This project is licensed under the MIT License.
```

harnesses/claude-mpm/output/level-5/task_board/seed.py
