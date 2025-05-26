from typing import Annotated

from fastapi import Depends, HTTPException, Security, security

from cache.accessor import get_redis_connection
from database.database import get_db_session
from exceptions import TokenExpired
from repository.cache import CacheRepository
from repository.category import CategoryRepository
from repository.task import TaskRepository
from repository.user import UserRepository
from service.task_service import TaskService
from service.user_service import UserService


def get_task_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_category_repository() -> CategoryRepository:
    db_session = get_db_session()
    return CategoryRepository(db_session)


def get_cache_repository() -> CacheRepository:
    db_conn = get_redis_connection()
    return CacheRepository(db_conn)


def get_task_service() -> TaskService:
    return TaskService(task_repository=get_task_repository(), cache_repository=get_cache_repository())


def get_user_repository() -> UserRepository:
    db_session = get_db_session()
    return UserRepository(db_session())


def get_user_service() -> UserService:
    return UserService()


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(user_service: Annotated[UserService, Depends(get_user_service)],
                        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)) -> int:
    try:
        user_id = user_service.get_user_id_from_access_token(token.credentials)
    except TokenExpired as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id
