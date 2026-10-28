# FastAPI Task API

A simple FastAPI application for managing tasks with in-memory storage.

## Features

- List all tasks
- Create a new task
- Replace an existing task
- Update selected task fields
- Delete a task

## Tech Stack

- Python
- FastAPI
- Uvicorn

## Project Structure

- `main.py` – FastAPI application and task endpoints
- `requirements.txt` – Python dependencies

## Setup

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the API

```bash
uvicorn main:app --reload
```

Then open the Swagger UI at:

- `http://127.0.0.1:8000/docs`

## API Endpoints

### GET /tasks
Returns all tasks.

### POST /tasks
Creates a new task.

Example body:

```json
{
  "title": "Write README",
  "completed": false
}
```

### PUT /tasks/{task_id}
Replaces a task by ID.

### PATCH /tasks/{task_id}
Updates selected fields on a task.

### DELETE /tasks/{task_id}
Deletes a task by ID.

## Notes

The application uses an in-memory list for persistence, so task data resets when the server restarts.
