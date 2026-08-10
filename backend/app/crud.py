from typing import Optional
from sqlmodel import Session, select

from app.models import Task, TaskCreate, TaskUpdate


def create_task(session: Session, task_data: TaskCreate) -> Task:
    # Convert the incoming (unsaved) schema into a real Task table row
    task = Task.model_validate(task_data)
    session.add(task)
    session.commit()
    session.refresh(task)  # pulls back DB-generated fields like id, created_at
    return task


def get_task(session: Session, task_id: int) -> Optional[Task]:
    # session.get() is a fast primary-key lookup — no need to build a
    # full SELECT query for this common case.
    return session.get(Task, task_id)


def get_tasks(
    session: Session,
    completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Task]:
    query = select(Task)
    if completed is not None:
        query = query.where(Task.completed == completed)
    query = query.offset(skip).limit(limit)
    return list(session.exec(query))


def update_task(session: Session, task: Task, task_data: TaskUpdate) -> Task:
    # exclude_unset=True: only fields the client actually sent get applied.
    # This is what makes partial updates (PATCH) work correctly.
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task: Task) -> None:
    session.delete(task)
    session.commit()