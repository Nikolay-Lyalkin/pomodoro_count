import json

from redis import Redis

from schemas.task import TaskSchema


class CacheRepository:

    def __init__(self, redis: Redis):
        self.redis = redis

    def set_task(self, tasks: list[TaskSchema]):
        with self.redis as redis:
            tasks_json = [task.json() for task in tasks]
            redis.lpush("task", *tasks_json)

    def get_tasks(self):
        with self.redis as redis:
            tasks = redis.lrange("task", 0, -1)
            tasks_schema = [TaskSchema.model_validate(json.loads(task)) for task in tasks]
        return tasks_schema
