from fastapi import APIRouter, Depends
from typing import Annotated

from repository.task import TaskRepository
from schemas.task import TaskSchema
from dependecy import get_task_repository, get_task_service
from service.task_service import TaskService

router = APIRouter(prefix="/task")


@router.get("/", response_model=list[TaskSchema])
async def get_task(task_service: Annotated[TaskService, Depends(get_task_service)]):
    tasks = task_service.get_task()
    return tasks


@router.post("/", response_model=TaskSchema)
async def post_task(task: TaskSchema,
                    task_repository: Annotated[TaskRepository, Depends(get_task_repository)]) -> TaskSchema:
    task = task_repository.create_task(task)
    return task


@router.patch("/{task_id}", response_model=TaskSchema)
async def patch_task(task_id: int, name: str,
                     task_repository: Annotated[TaskRepository, Depends(get_task_repository)]) -> TaskSchema | str:
    task = task_repository.patch_task(task_id, name)
    return task


@router.delete("/{task_id}")
async def delete_task(task_id: int, name: str,
                      task_repository: Annotated[TaskRepository, Depends(get_task_repository)]):
    task = task_repository.delete_task(task_id)

    return f"Задача {name} успешно удалена"
