from sqlalchemy import select

from database.models import Task
from exceptions import TaskNotFound
from repository.cache import CacheRepository
from repository.task import TaskRepository
from schemas.task import TaskSchema


class TaskService:

    def __init__(self, task_repository: TaskRepository,
                 cache_repository: CacheRepository):
        self.task_repository = task_repository
        self.cache_repository = cache_repository

    def get_task(self):
        if tasks := self.cache_repository.get_tasks():
            return tasks
        tasks = self.task_repository.get_tasks()
        tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
        self.cache_repository.set_task(tasks_schema)
        return tasks
