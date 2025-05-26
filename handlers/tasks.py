from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from dependecy import get_task_repository, get_task_service, get_request_user_id
from exceptions import TaskNotFound
from repository.task import TaskRepository
from schemas.task import TaskSchema
from service.task_service import TaskService

router = APIRouter(prefix="/task")


@router.get("/", response_model=list[TaskSchema])
async def get_task(task_service: Annotated[TaskService, Depends(get_task_service)]):
    tasks = task_service.get_task()
    return tasks


@router.post("/", response_model=TaskSchema)
async def post_task(task: TaskSchema,
                    task_repository: Annotated[TaskRepository, Depends(get_task_repository)],
                    user_id: int = Depends(get_request_user_id)) -> TaskSchema:
    task = task_repository.create_task(task, user_id)
    return task


@router.patch("/{task_id}", response_model=TaskSchema)
async def patch_task(task_id: int, name: str,
                     task_repository: Annotated[TaskRepository, Depends(get_task_repository)],
                     user_id: int = Depends(get_request_user_id)) -> TaskSchema | HTTPException:
    try:
        task = task_repository.patch_task(task_id=task_id, name=name, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return task


@router.delete("/{task_id}")
async def delete_task(task_id: int,
                      task_repository: Annotated[TaskRepository, Depends(get_task_repository)],
                      user_id: int = Depends(get_request_user_id)
                      ) -> str | dict:
    try:
        task = task_repository.delete_task(task_id, user_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return f"Задача успешно удалена"
