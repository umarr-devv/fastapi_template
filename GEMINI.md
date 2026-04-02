# Project Guide for AI Assistants

This document describes the **conceptual architecture** of the project and provides instructions to help AI assistants work effectively within the codebase. Read this before making any changes.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI (async) |
| ORM | SQLAlchemy 2.x (async) |
| Database | PostgreSQL via `asyncpg` |
| Validation | Pydantic v2 |
| Auth | JWT (PyJWT) + bcrypt |
| Caching | aiocache (Redis) |
| Migrations | Alembic |
| Server | Uvicorn / Hypercorn |
| Config | pydantic-settings (env-based) |
| Testing | pytest + pytest-asyncio + httpx |

Python version: **3.13+**. Use modern Python features (e.g., `X | None` instead of `Optional[X]`, `list[X]` instead of `List[X]`).

---

## Project Layout

```
src/
├── main.py                  # FastAPI app factory, middleware registration
├── api/
│   ├── __init__.py          # Top-level APIRouter aggregating all versions
│   └── v1/
│       ├── endpoints/       # Route handlers (thin controllers)
│       ├── schemas/         # Pydantic input/output models
│       ├── repository/      # DB access layer (queries & mutations)
│       └── dependencies/    # FastAPI Depends() factories
├── core/
│   ├── config.py            # pydantic-settings config groups
│   ├── cache.py             # Cache initialization
│   ├── error.py             # Global exception handler registration
│   ├── logger.py            # Logging setup
│   └── paths.py             # Filesystem path constants
├── db/
│   ├── base.py              # Declarative base with shared columns
│   └── database.py          # Async engine + session factory
├── models/                  # SQLAlchemy ORM models
├── services/                # Pure business logic, no DB/HTTP concerns
├── middlewares/             # Custom ASGI middlewares (CORS, API logging, etc.)
├── websocket/               # WebSocket routers
└── files/                   # Local file storage root

tests/                       # pytest test suite, mirrors src/ structure
alembic/                     # Migration scripts
```

---

## Architecture Concepts

### 1. Database Models (`src/db/base.py`, `src/models/`)

Every ORM model **must** inherit from the shared `Base` class.  
`Base` automatically provides:
- `id` — UUID v7 string primary key (sortable by time, globally unique)
- `is_deleted` — soft-delete flag; records are never physically removed
- `create_at` / `update_at` — UTC-aware timestamps managed by the ORM

> **Rule:** Never delete rows physically. Always set `is_deleted = True`.  
> **Rule:** Never use `int` or `uuid4` for primary keys. Always use UUID v7 via `Base.uuid()`.

### 2. Configuration (`src/core/config.py`)

Configuration is split into **domain-scoped settings classes**, each extending `BaseSettings` with a dedicated `env_prefix`. A single `ConfigModel` aggregates them all and is instantiated once as `config`.

> **Rule:** Add new settings in a new or existing scoped class. Never add raw `os.getenv()` calls; always go through `config`.

### 3. Repository Layer (`src/api/v1/repository/`)

Repositories handle all database interactions for a specific model. They are generic — there is a `BaseRepository[T]` providing common operations. Domain-specific repositories inherit from it and add custom queries.

A `RepositoriesManager` aggregates all repositories and is injected into endpoints via FastAPI `Depends`.

> **Rule:** No raw SQL or ORM queries inside endpoints or services. All DB access goes through a repository.  
> **Rule:** Repositories receive an `AsyncSession` injected via dependency injection — they never create or manage sessions themselves.

### 4. Schemas (`src/api/v1/schemas/`)

Pydantic models for request/response. Organized per domain, with sub-directories where a domain has multiple schemas (e.g., `user/`, `file/`).

A `BaseSchema` exists for read responses, mirroring `Base`'s `id`, `create_at`, `update_at`.

> **Rule:** Response schemas extend `BaseSchema`.  
> **Rule:** Request schemas (Create, Patch) do not inherit from `BaseSchema`.  
> **Rule:** Use `from __future__ import annotations` and Pydantic v2 features (e.g., `model_validator`, `field_validator`).

### 5. Endpoints (`src/api/v1/endpoints/`)

Endpoints are **thin controllers**: they validate input, call repositories or services, and return responses. Business logic does not live here.

Each endpoint file defines its own `APIRouter` with a prefix and tags. Routers are aggregated into a versioned router in `api/v1/__init__.py` and then into `api/__init__.py`.

> **Rule:** Handlers should be short (ideally under 20 lines). Extract logic into services or repositories.  
> **Rule:** Always set `operation_id` on every route for clean OpenAPI/SDK generation.  
> **Rule:** Handlers are named `on_<verb>_<resource>` (e.g., `on_create_user`, `on_get_file`).

### 6. Dependencies (`src/api/v1/dependencies/`)

Reusable FastAPI `Depends()` factories. Auth resolution, session creation, and manager injection live here.

> **Rule:** `get_manager` provides the `RepositoriesManager`. Use it in every route that accesses the DB.  
> **Rule:** `get_user` (or equivalent) resolves the authenticated user from the JWT. Use it in every protected route.

### 7. Services (`src/services/`)

Pure business logic — stateless utilities with no direct DB or HTTP calls. Examples: password hashing, JWT encoding/decoding, file handling.

> **Rule:** Services are stateless. No session, no request object inside services.

### 8. Middlewares (`src/middlewares/`)

Custom ASGI middlewares registered in `main.py`. Examples: CORS, structured API access logging.

> **Rule:** Only register middleware in `main.py`. Middleware files only define the class.

---

## Coding Conventions

- **Async everywhere.** All endpoint handlers, repository methods, DB calls must be `async def`.
- **Type annotations are mandatory.** All function signatures must be fully annotated, including return types.
- **No raw `import *` in production code.** The `*` imports in endpoints are acceptable only for intra-module aggregations via explicit `__all__` in `__init__.py`.
- **Dependency injection via `Annotated`.** Prefer `Annotated[Type, Depends(...)]` over the older `= Depends(...)` style.
- **Soft deletes.** Use `is_deleted` flag; filter it out in all read queries.
- **Error handling.** Raise `HTTPException` with meaningful `status_code` and `detail`. The global handler in `core/error.py` logs all exceptions — do not add redundant logging in individual endpoints.
- **Formatting.** Code is formatted with `black`. Run `black src/` before committing.
- **Linting.** `mypy` is configured. Ensure no new type errors are introduced.

---

## Common Commands

```bash
# Start development server
uvicorn src.main:app --reload --port 8000

# Run with Hypercorn (production-like)
hypercorn src.main:app --config hypercorn.toml

# Run tests
pytest

# Apply migrations
alembic upgrade head

# Create a new migration
alembic revision --autogenerate -m "description"

# Format code
black src/

# Type-check
mypy src/
```

---

## Adding a New Resource — Checklist

When adding a completely new domain entity (e.g., a new data resource), follow this order:

1. **`src/models/`** — Create the ORM model extending `Base`.
2. **`alembic/`** — Generate a migration (`alembic revision --autogenerate`).
3. **`src/api/v1/schemas/<resource>/`** — Create `BaseSchema`, `Create...Schema`, `Patch...Schema`, etc.
4. **`src/api/v1/repository/<resource>.py`** — Create a repository extending `BaseRepository`.
5. **`src/api/v1/repository/manager.py`** — Register the new repository in `RepositoriesManager`.
6. **`src/api/v1/endpoints/<resource>.py`** — Create the `APIRouter` with route handlers.
7. **`src/api/v1/__init__.py`** — Include the new router.
8. **`tests/`** — Add tests mirroring the structure above.

---

## Key Anti-Patterns to Avoid

| ❌ Don't | ✅ Do instead |
|---|---|
| Physical row deletion | Soft-delete via `is_deleted = True` |
| Business logic in endpoints | Move to services or repositories |
| Raw `os.getenv()` anywhere | Use `config.<group>.<key>` |
| Blocking I/O in async handlers | Use async libraries (`aiofiles`, `asyncpg`, etc.) |
| Session created inside a repository | Inject `AsyncSession` via `Depends` |
| `int` or UUID4 as primary keys | UUID7 via `Base.uuid()` |
| Magic strings for status codes | `from fastapi import status` constants |
| Missing `operation_id` on routes | Always set `operation_id` |
