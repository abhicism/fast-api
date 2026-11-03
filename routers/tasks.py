from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from crud import task as task_crud
from database.database import get_db
from schemas.task import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    return task_crud.get_tasks(db)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_crud.create_task(db, task)


@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def replace_task(task_id: int, changes: TaskCreate, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_crud.update_task(db, task, TaskUpdate(**changes.model_dump()))


@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(task_id: int, changes: TaskUpdate, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_crud.update_task(db, task, changes)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: int, db: Session = Depends(get_db)):
    task = task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task_crud.delete_task(db, task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
