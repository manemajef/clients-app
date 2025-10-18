# Backend Architecture - Layered Structure

## Overview

This backend follows a **layered architecture** pattern with clear separation of concerns:

```
┌─────────────────────────────────────┐
│   API Routes (Presentation Layer)   │  HTTP requests/responses
├─────────────────────────────────────┤
│   Services (Business Logic Layer)   │  Business rules & orchestration
├─────────────────────────────────────┤
│   Repositories (Data Access Layer)  │  Database queries
├─────────────────────────────────────┤
│   Models (Domain Layer)             │  Data structures
└─────────────────────────────────────┘
         ↓
    Database (SQLite)
```

**Key Principle:** Each layer only imports from layers below it. Never upward.

---

## Layer Responsibilities

### 1. Models (`app/models/`)
**What they are:** Pure data structures (SQLModel/Pydantic classes)

**Responsibilities:**
- Define database table schemas
- Define API request/response schemas
- Define relationships between entities
- Define field validation rules

**What they DON'T do:**
- Business logic
- Database queries
- Import from services or repositories

**Example:**
```python
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=utc_now)
    clients: list['Client'] = Relationship(back_populates="user")
```

---

### 2. Repositories (`repositories/`)
**What they are:** Data access abstraction layer

**Responsibilities:**
- Execute SQL queries (SELECT, INSERT, UPDATE, DELETE)
- Handle database session operations (add, flush, refresh)
- Provide reusable query methods
- Encapsulate all SQLModel/SQLAlchemy operations

**What they DON'T do:**
- Business logic or validation
- Commit transactions (services handle this)
- Call other repositories
- Raise HTTP exceptions

**Transaction Rule:** Repositories use `flush()` and `refresh()`, but never `commit()`. Services manage commits.

**Example:**
```python
class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.exec(select(User).where(User.email == email)).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()  # NOT commit()
        self.db.refresh(user)
        return user
```

---

### 3. Services (`app/services/`)
**What they are:** Business logic layer

**Responsibilities:**
- Implement business rules and validation
- Orchestrate multiple repository calls
- Manage transaction boundaries (`commit()` or `rollback()`)
- Handle cross-entity operations
- Raise domain-specific exceptions

**What they DON'T do:**
- Execute raw SQL queries
- Import from routes/API layer
- Handle HTTP-specific logic (status codes, etc.)

**Transaction Rule:** Services are responsible for calling `db.commit()` after repository operations.

**Example:**
```python
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user: UserCreate) -> User:
        # Business logic: check email is unique
        if self.user_repo.get_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email is taken")

        # Create user
        db_user = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=hash_password(user.password)
        )
        created_user = self.user_repo.create(db_user)

        # Service manages commit
        self.user_repo.db.commit()

        return created_user
```

---

### 4. API Routes (`app/api/routes/`)
**What they are:** HTTP request handlers

**Responsibilities:**
- Define HTTP endpoints (GET, POST, etc.)
- Parse request data (path params, query params, body)
- Call service methods
- Return HTTP responses
- Handle HTTP-specific errors (status codes)
- Define response models

**What they DON'T do:**
- Business logic
- Database queries
- Complex data manipulation

**Example:**
```python
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user)
```

---

### 5. Dependencies (`app/api/deps.py`)
**What they are:** Dependency injection providers

**Responsibilities:**
- Create database sessions
- Instantiate repositories with sessions
- Instantiate services with repositories
- Handle authentication (get current user)
- Provide reusable dependencies for routes

**Example:**
```python
def get_db():
    with Session(engine) as db:
        yield db

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo)
```

---

## Request Workflow Example

### User Registration Flow

1. **Client sends POST request** to `/auth/register`
   ```json
   {"email": "test@example.com", "password": "secret", "full_name": "Test User"}
   ```

2. **Route layer** (`auth.py`)
   - Receives request
   - FastAPI validates request body against `UserCreate` schema
   - Injects `UserService` via `Depends(get_user_service)`
   - Calls `user_service.create_user(user)`

3. **Dependency Injection** (`deps.py`)
   - `get_db()` creates database session
   - `get_user_repository()` creates `UserRepository(db)`
   - `get_user_service()` creates `UserService(user_repo)`

4. **Service layer** (`user_service.py`)
   - Checks if email already exists via `user_repo.get_by_email()`
   - Hashes password
   - Creates `User` model instance
   - Calls `user_repo.create(user)`
   - **Commits transaction** via `user_repo.db.commit()`
   - Returns created user

5. **Repository layer** (`user_repository.py`)
   - Executes `db.exec(select(User).where(...))` for email check
   - Executes `db.add(user)` + `db.flush()` + `db.refresh()` for creation
   - Returns user object

6. **Route layer**
   - Receives user from service
   - FastAPI serializes to `UserResponse` model
   - Returns JSON response

---

## Dependency Flow

```
Route
  ↓ depends on
Service
  ↓ depends on
Repository
  ↓ depends on
Database Session
  ↓ connects to
Database
```

**Example for Client Creation:**
```python
# Route needs ClientService
def add_client(client: ClientAdd, client_service: ClientService = Depends(...)):
    ...

# ClientService needs 3 repositories
class ClientService:
    def __init__(
        self,
        client_repo: ClientRepository,
        contact_repo: ContactRepository,
        user_repo: UserRepository  # For validation
    ):
        ...

# Each repository needs database session
class ClientRepository:
    def __init__(self, db: Session):
        ...
```

---

## Import Rules

### ✓ Allowed Imports

```python
# Models can import from:
from app.core.utils import utc_now

# Repositories can import from:
from app.models.user import User
from sqlmodel import Session, select

# Services can import from:
from repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import hash_password

# Routes can import from:
from app.services.user_service import UserService
from app.api.deps import get_user_service
from app.models.user import UserCreate
```

### ✗ Forbidden Imports

```python
# Models should NOT import:
from app.services.user_service import ...  # ✗ Circular dependency
from repositories.user_repository import ... # ✗ Wrong layer

# Repositories should NOT import:
from app.services.client_service import ... # ✗ Upward dependency
from repositories.client_repository import ... # ✗ Cross-repository dependency

# Services should NOT import:
from app.api.routes.auth import ... # ✗ Upward dependency
```

---

## Key Design Decisions

### 1. Why Separate Repositories?
- **Testability:** Can mock repositories easily for service tests
- **Flexibility:** Can swap database implementations without changing services
- **Reusability:** Same query logic used across multiple services
- **Single Responsibility:** Query logic separated from business logic

### 2. Why Services Don't Commit?
**Actually they DO.** Repositories use `flush()`, services use `commit()`.

**Why?**
- Services orchestrate multiple repository calls
- If second operation fails, we can rollback the whole transaction
- Example:
  ```python
  # In service:
  client = client_repo.create(client)  # flush only
  contact_repo.create_many(contacts)   # flush only
  client_repo.db.commit()              # commit both at once
  ```

### 3. Why Dependency Injection?
- **Loose Coupling:** Routes don't know how services are created
- **Testability:** Easy to inject mock services/repositories
- **Automatic Cleanup:** FastAPI handles session cleanup
- **Consistency:** Same session shared across all repos in one request

---

## Common Patterns

### Pattern 1: Validation in Service
```python
# Service validates business rules
def create_client(self, user_email: str, client_data: ClientAdd):
    user = self.user_repo.get_by_email(user_email)
    if not user:
        return None  # or raise exception

    existing = self.client_repo.get_by_user_and_name(user.id, client_data.name)
    if existing:
        return None  # duplicate name

    # Proceed with creation...
```

### Pattern 2: Multi-Entity Operations
```python
# Service coordinates multiple repositories
def add_client(self, user_email: str, client: ClientAdd):
    # Use user repo to validate
    user = self.user_repo.get_by_email(user_email)

    # Use client repo to create client
    created_client = self.client_repo.create(Client(...))

    # Use contact repo to create contacts
    self.contact_repo.create_many([...])

    # Commit all at once
    self.client_repo.db.commit()
```

### Pattern 3: Ownership Validation
```python
# Service checks ownership before allowing operation
def add_meeting(self, meeting: MeetingCreate):
    # Validate user exists
    user = self.user_repo.get_by_id(meeting.user_id)
    if not user:
        return None

    # Validate user owns the client
    if meeting.client_id:
        client = self.client_repo.get_by_id(meeting.client_id)
        if not client or client.user_id != meeting.user_id:
            return None  # User doesn't own this client

    # Proceed...
```

---

## File Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependency injection
│   │   └── routes/
│   │       ├── auth.py          # Auth endpoints
│   │       ├── admin.py         # Admin endpoints
│   │       └── client.py        # Client endpoints
│   ├── core/
│   │   ├── config.py            # Settings
│   │   ├── security.py          # Password/JWT functions
│   │   └── utils.py             # Shared utilities (utc_now)
│   ├── models/
│   │   ├── user.py              # User models
│   │   ├── client.py            # Client & Contact models
│   │   └── meeting.py           # Meeting models
│   ├── services/
│   │   ├── user_service.py      # User business logic
│   │   ├── client_service.py    # Client business logic
│   │   └── meeting_service.py   # Meeting business logic
│   ├── database.py              # Database engine setup
│   └── main.py                  # FastAPI app
├── repositories/
│   ├── user_repository.py       # User data access
│   ├── client_repository.py     # Client & Contact data access
│   └── meeting_repository.py    # Meeting data access
└── STRUCTURE.md                 # This file
```

---

## Benefits of This Architecture

1. **Maintainability:** Clear responsibilities, easy to find code
2. **Testability:** Each layer can be tested independently
3. **Flexibility:** Can swap implementations without affecting other layers
4. **Scalability:** Easy to add new features following same pattern
5. **Team Collaboration:** Different developers can work on different layers
6. **Code Reuse:** Repository queries used by multiple services
7. **Clean Imports:** No circular dependencies or layer violations
