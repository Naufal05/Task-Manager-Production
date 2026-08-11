from typing import Optional
from sqlmodel import Session, select

from app.models import Task, TaskCreate, TaskUpdate


def create_task(session: Session, task_data: TaskCreate, owner_id: int) -> Task:
    # owner_id comes from the AUTHENTICATED USER (via get_current_user),
    # never from the client's request body -- see models.py's TaskCreate,
    # which has no owner_id field at all.
    task = Task.model_validate(task_data, update={"owner_id": owner_id})
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task(session: Session, task_id: int, owner_id: int) -> Optional[Task]:
    task = session.get(Task, task_id)
    # Ownership check: even if the task_id exists, only return it if it
    # belongs to the requesting user. Otherwise treat it as if it doesn't
    # exist -- this is what makes GET /tasks/7 on someone ELSE's task 404,
    # not 403. Not leaking "this exists but isn't yours" is intentional.
    if task is None or task.owner_id != owner_id:
        return None
    return task


def get_tasks(
    session: Session,
    owner_id: int,
    completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Task]:
    query = select(Task).where(Task.owner_id == owner_id)
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