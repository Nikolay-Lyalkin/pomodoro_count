from fastapi import APIRouter, Depends
from typing import Annotated

from dependecy import get_category_repository
from repository.category import CategoryRepository
from schemas.category import CategorySchema
from fixtures import categories
from database.database import get_db_session

router = APIRouter(prefix="/category")


@router.get("/{category_id}")
async def get_category(category_id: int, category_repo: Annotated[CategoryRepository, Depends(get_category_repository)]) -> CategorySchema:
    category = category_repo.get_category(category_id)
    return category


@router.get("/all/category")
async def get_categories(category_repo: Annotated[CategoryRepository, Depends(get_category_repository)]) -> list[CategorySchema]:
    category = category_repo.get_categories()
    return category


@router.post("/")
def post_category(category: CategorySchema, category_repo: Annotated[CategoryRepository, Depends(get_category_repository)]) -> CategorySchema:
    category = category_repo.create_category(category)
    return category


@router.patch("/{category_id}")
def patch_category(category_id: int, name: str, category_repo: Annotated[CategoryRepository, Depends(get_category_repository)]) -> CategorySchema | str:
    category = category_repo.patch_category(category_id, name)
    return category


@router.delete("/{category_id}")
def delete_category(category_id: int, category_repo: Annotated[CategoryRepository, Depends(get_category_repository)]) -> str:
    category_repo.delete_category(category_id)
    return f" Категория успешно удалена"
