from typing import Annotated

from fastapi import APIRouter, Depends

from repository.user import UserRepository
from schemas.user import UserLoginOrCreate, UserSchema
from dependecy import get_user_repository


router = APIRouter(prefix="/user")


@router.post("/", response_model=UserSchema)
async def post_user(user: UserLoginOrCreate,
                    user_repository: Annotated[UserRepository, Depends(get_user_repository)]) -> UserSchema:
    user = user_repository.create_user(user.username, user.password)
    return user
