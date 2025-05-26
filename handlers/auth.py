from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from dependecy import get_user_repository
from exceptions import UserNotFound
from repository.user import UserRepository
from schemas.user import UserLoginOrCreate, UserSchema

router = APIRouter(prefix="/auth")


@router.post("/", response_model=UserSchema)
async def post_user(user: UserLoginOrCreate,
                    user_repository: Annotated[UserRepository, Depends(get_user_repository)]) -> UserSchema:
    try:
        user = user_repository.login_user(user.username, user.password)
    except UserNotFound as ex:
        raise HTTPException(
            status_code=404,
            detail=ex.detail
        )
    return user
