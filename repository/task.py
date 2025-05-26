from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from database.models import Task
from exceptions import TaskNotFound
from schemas.task import TaskSchema


class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self) -> list[Task]:
        query = select(Task)
        with self.db_session() as session:
            tasks = session.execute(query).scalars().all()
        return tasks

    def get_task(self, task_id) -> Task:
        query = select(Task).where(Task.id == task_id)
        with self.db_session() as session:
            task = session.execute(query).scalar()
        return task

    def create_task(self, task: TaskSchema, user_id: int) -> TaskSchema:
        task_model_alchemy = Task(id=task.id, name=task.name, pomodoro_count=task.pomodoro_count,
                                  category_id=task.category_id, user_id=user_id)
        with self.db_session() as session:
            session.add(task_model_alchemy)
            session.commit()
        return task

    def patch_task(self, task_id: int, user_id: int, name: str) -> Task:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        with self.db_session() as session:
            task = session.execute(query).scalars().one_or_none()
        if not task:
            raise TaskNotFound
        query = update(Task).where(Task.id == task_id).values(name=name).returning(Task)
        with self.db_session() as session:
            session.execute(query)
            session.commit()
        return self.get_task(task_id)

    def delete_task(self, task_id: int, user_id: int) -> None:
        self.get_user_task(task_id=task_id, user_id=user_id)
        query = delete(Task).where(Task.id == task_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()

    def get_user_task(self, task_id: int, user_id: int) -> Task:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        with self.db_session() as session:
            task = session.execute(query).scalars().one_or_none()
        if not task:
            raise TaskNotFound
