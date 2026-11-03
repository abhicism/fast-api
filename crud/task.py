from sqlalchemy import select
from sqlalchemy.orm import Session

from models.task import TaskDB
from schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session) -> list[TaskDB]:
    return list(db.scalars(select(TaskDB)).all())


def get_task(db: Session, task_id: int) -> TaskDB | None:
    return db.get(TaskDB, task_id)


def create_task(db: Session, task: TaskCreate) -> TaskDB:
    new_task = TaskDB(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(db: Session, task: TaskDB, changes: TaskUpdate) -> TaskDB:
    for field, value in changes.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: TaskDB) -> None:
    db.delete(task)
    db.commit()
