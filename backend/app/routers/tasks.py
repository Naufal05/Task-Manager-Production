from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_session
from app.models import TaskCreate, TaskRead, TaskUpdate
from app import crud

# APIRouter lets us group related endpoints and mount them onto the main
# app with a shared prefix/tags, instead of cramming everything into main.py.
router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    """
    REQUEST BODY example:
    task: TaskCreate  -> FastAPI reads the JSON body, validates it against
    the TaskCreate schema (title required, priority must be a valid enum, etc.)
    and gives us a fully-validated Python object here. Invalid input never
    reaches this line -- FastAPI returns a 422 automatically.
    """
    return crud.create_task(session, task)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    """
    QUERY PARAMETERS example:
    completed, skip, limit are all query parameters because they are
    simple types with default values and are NOT part of the URL path.
    Example calls:
      GET /tasks                -> all tasks
      GET /tasks?completed=true -> only completed tasks
      GET /tasks?skip=10&limit=5 -> pagination
    """
    return crud.get_tasks(session, completed=completed, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)):

    """
    PATH PARAMETER example:
    task_id is part of the URL itself (e.g. /tasks/7), not a query string.
    FastAPI extracts it, converts it to int (or 422s if it can't), and
    passes it straight into the function.
    """
    task = crud.get_task(session, task_id)
    if task is None:
        # ERROR HANDLING example: raising HTTPException immediately stops
        # execution and returns a proper JSON error response with the
        # given status code -- no manual response-building needed.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    task = crud.get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return crud.update_task(session, task, task_update)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = crud.get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    crud.delete_task(session, task)
    return None