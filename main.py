
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define the structure of a task
class Task(BaseModel):
    title: str
    completed: bool = False

# Temporary storage
tasks = [
    {"id": 1, "title": "Learn FastAPI", "completed": False}
]

# GET: Retrieve all tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# POST: Create a task
@app.post("/tasks")
def create_task(task: Task):
    new_task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        **task.model_dump() 
    }
    tasks.append(new_task)
    return new_task

# PUT: Replace a task completely
@app.put("/tasks/{task_id}")
def replace_task(task_id: int, task: Task):
    for index, existing in enumerate(tasks):
        if existing["id"] == task_id:
            tasks[index] = {"id": task_id, **task.model_dump()}
            return tasks[index]

    raise HTTPException(status_code=404, detail="Task not found")

# PATCH: Update selected task fields
@app.patch("/tasks/{task_id}")
def update_task(task_id: int, changes: dict):
    for task in tasks:
        if task["id"] == task_id:
            task.update(changes)
            return task

    raise HTTPException(status_code=404, detail="Task not found")

# DELETE: Remove a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}

    raise HTTPException(status_code=404, detail="Task not found")
