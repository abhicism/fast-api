# TaskFlow API

A FastAPI task manager backed by SQLite and SQLAlchemy.

## Project structure

- `main.py` — creates the FastAPI app and registers the routes.
- `database/database.py` — configures SQLite and request-scoped sessions.
- `models/task.py` — SQLAlchemy task table model.
- `schemas/task.py` — request validation and response schemas.
- `routers/tasks.py` — HTTP endpoints for task operations.
- `crud/task.py` — database create, read, update, and delete operations.

## Setup and run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.
The SQLite database is stored in `taskflow.db` in the project directory.

## Endpoints

- `GET /` — health check.
- `GET /tasks` — list tasks.
- `POST /tasks` — create a task (`title` required; `completed` defaults to `false`).
- `GET /tasks/{task_id}` — retrieve one task.
- `PUT /tasks/{task_id}` — replace a task.
- `PATCH /tasks/{task_id}` — update provided task fields.
- `DELETE /tasks/{task_id}` — delete a task.
