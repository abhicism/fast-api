
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create the FastAPI application
app = FastAPI(title="TaskFlow API")


# Pydantic model: validates incoming task data
class Task(BaseModel):
    title: str
    completed: bool = False

# Define the structure of a task response
class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

# Temporary in-memory task storage
tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    }
]


# GET: Welcome endpoint
@app.get("/")
def home():
    return {"message": "Welcome to TaskFlow API"}


# GET: Retrieve all tasks
@app.get("/tasks")
def get_tasks(completed: bool | None = None):
    if completed is None:
        return tasks

    return [
        task for task in tasks
        if task["completed"] == completed
    ]

# Return a validated task response
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# GET: Retrieve a single task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# POST: Create a new task
@app.post("/tasks", status_code=201)
def create_task(task: Task):
    new_task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        **task.model_dump()
    }

    tasks.append(new_task)
    return new_task


# PUT: Replace an existing task completely
@app.put("/tasks/{task_id}")
def replace_task(task_id: int, task: Task):
    for index, existing_task in enumerate(tasks):
        if existing_task["id"] == task_id:
            updated_task = {
                "id": task_id,
                **task.model_dump()
            }

            tasks[index] = updated_task
            return updated_task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# PATCH: Update selected task fields
@app.patch("/tasks/{task_id}")
def update_task(task_id: int, changes: dict):
    allowed_fields = {"title", "completed"}

    # Reject unsupported fields
    invalid_fields = set(changes) - allowed_fields
    if invalid_fields:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid fields: {sorted(invalid_fields)}"
        )

    # Validate changes using the Pydantic model
    try:
        validated_changes = Task.model_validate(
            {
                "title": "Temporary title",
                **changes
            }
        ).model_dump(exclude_unset=False)

        # Keep only fields actually supplied by the client
        validated_changes = {
            key: value
            for key, value in validated_changes.items()
            if key in changes
        }
    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Invalid task data"
        )

    for task in tasks:
        if task["id"] == task_id:
            task.update(validated_changes)
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# DELETE: Remove a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
