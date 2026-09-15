# Yuz Tut Backend

Backend service for the **Yuz Tut** project.

This repository contains the backend API responsible for application logic, user authentication, database communication, and supporting services.

The backend is being developed incrementally. This README describes the current implementation and will be updated as new functionality is added.

---

## Current Status

The backend foundation has been initialized.

Currently implemented:

- FastAPI application
- Docker-based development environment
- PostgreSQL database
- Redis service
- Asynchronous SQLAlchemy database connection
- Alembic migration setup
- User registration
- User login
- Password hashing
- JWT access tokens
- JWT refresh tokens

The project is still under active development.

---

## Technology Stack

- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Redis
- Pydantic
- JWT authentication
- Docker
- Docker Compose

---

## Project Structure

```text
backend/
├── app/
│   ├── core/
│   │   └── security.py
│   ├── database/
│   │   └── session.py
│   │   └── base.py
│   ├── models/
│   │   └── user.py
│   ├── repositories/
│   │   └── user_repository.py
│   ├── routes/
│   │   └── auth.py
│   ├── schemas/
│   │   └── auth.py
│   ├── services/
│   │   └── auth_service.py
│   ├── config.py
│   └── main.py
├── alembic/
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Application Layers

- **Routes:** API endpoints and HTTP request/response handling.
- **Services:** Business logic, including registration and authentication.
- **Repositories:** Database operations such as retrieving and creating users.
- **Models:** SQLAlchemy database models.
- **Schemas:** Pydantic request and response models.
- **Core:** Shared functionality such as security and token handling.
- **Database:** Database engine and session configuration.

---

## Requirements

Install the following tools:

- Docker
- Docker Compose
- Git

Python is also required for local development.

The current development environment uses:

```text
Python 3.14.4
```

---

## Environment Configuration

Create a `.env` file in the backend root directory.

Example:

```env
APP_NAME=Yuz Tut Backend
APP_ENV=development
DEBUG=true

DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/yuz_tut

REDIS_URL=redis://redis:6379/0

SECRET_KEY=replace_with_a_secure_secret_key
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

The exact variable names and values must match the current application configuration.

> Do not commit the `.env` file to Git.

---

## Running the Backend

Navigate to the backend directory:

```bash
cd ~/working-directory/yuz_tut/backend
```

### Build and Start Services

```bash
docker compose up --build
```

### Start in Detached Mode

```bash
docker compose up -d
```

### View Logs

```bash
docker compose logs -f
```

### Stop Services

```bash
docker compose down
```

### Stop Services and Remove Volumes

```bash
docker compose down -v
```

> Warning: Removing volumes may delete local PostgreSQL data.

---

## Services

### API

The FastAPI application runs at:

```text
http://localhost:8000
```

### PostgreSQL

PostgreSQL is used as the primary relational database.

The API connects to PostgreSQL asynchronously through SQLAlchemy.

### Redis

Redis is included as a supporting service for caching and other backend functionality.

---

## API Documentation

When the application is running, Swagger documentation is available at:

```text
http://localhost:8000/docs
```

ReDoc documentation is available at:

```text
http://localhost:8000/redoc
```

---

## Authentication

The current authentication implementation supports user registration and login.

### Register a User

```http
POST /auth/register
```

Example request:

```json
{
  "email": "test@example.com",
  "username": "testuser",
  "password": "TestPassword123"
}
```

Example response:

```json
{
  "id": "user-uuid",
  "email": "test@example.com",
  "username": "testuser",
  "is_active": true
}
```

Passwords are hashed before being stored in the database.

### Login

```http
POST /auth/login
```

Example request:

```json
{
  "email": "test@example.com",
  "password": "TestPassword123"
}
```

Example response:

```json
{
  "access_token": "jwt-access-token",
  "refresh_token": "jwt-refresh-token",
  "token_type": "bearer"
}
```

The login endpoint verifies user credentials and returns an access token and refresh token.

---

## Database

The project uses:

- PostgreSQL as the database
- SQLAlchemy as the ORM
- Async SQLAlchemy sessions for database access
- Alembic for database migrations

The database session is configured using an asynchronous engine and `AsyncSession`.

---

## Database Migrations

Alembic is used to manage database schema changes.

### Create a Migration

After changing a database model:

```bash
alembic revision --autogenerate -m "describe the change"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Roll Back the Latest Migration

```bash
alembic downgrade -1
```

Database migrations should be committed together with the model changes that require them.

---

## Development Workflow

1. Create a separate feature branch.
2. Implement the change.
3. Run the backend using Docker Compose.
4. Test the affected endpoints through Swagger or an API client.
5. Check the application logs.
6. Update the documentation if necessary.
7. Commit the changes.
8. Push the branch.
9. Open a pull request.

Example:

```bash
git checkout -b feature/add-authenticated-user
```

```bash
git status
```

```bash
git add .
```

```bash
git commit -m "feat: add authenticated user endpoint"
```

```bash
git push origin feature/add-authenticated-user
```

---

## Commit Message Convention

Use clear and descriptive commit messages.

Recommended format:

```text
type: short description
```

Common commit types:

| Type | Purpose |
|---|---|
| `feat` | Add a new feature |
| `fix` | Fix a bug |
| `docs` | Documentation changes |
| `refactor` | Code restructuring |
| `test` | Add or update tests |
| `chore` | Maintenance or configuration |
| `perf` | Performance improvements |

Examples:

```text
feat: add user registration endpoint
fix: correct JWT access token response
docs: update backend README
refactor: separate authentication logic from routes
```

---

## Current API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Authenticate a user and return JWT tokens |

This table will be updated whenever new endpoints are added.

---

## Planned Improvements

The following features are planned but are not yet completed:

- JWT authentication dependency
- Authenticated user endpoint
- Token refresh endpoint
- User profile functionality
- Search functionality
- Search history
- AI model integration
- Automated tests
- Improved error handling
- Production configuration
- Deployment preparation

---

## Security Guidelines

- Do not commit `.env` files.
- Do not expose secrets in source code.
- Never store plain-text passwords.
- Use secure secret keys.
- Validate all incoming requests.
- Protect authenticated routes with JWT verification.
- Disable debug mode in production.
- Review database migrations before applying them to production.

---

## Contribution

All backend changes should be submitted through a pull request.

Each pull request should include:

- A clear description of the change
- The reason for the change
- Testing information
- Database migration details, if applicable
- API changes, if applicable
- Relevant documentation updates

The pull request template is located at:

```text
.github/pull_request_template.md
```

---

## License

License information will be added later.