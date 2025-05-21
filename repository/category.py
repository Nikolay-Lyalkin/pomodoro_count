from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from database.models import Category
from schemas.category import CategorySchema


class CategoryRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_category(self, category_id: int) -> Category:
        query = select(Category).where(Category.id == category_id)
        with self.db_session() as session:
            category = session.execute(query).scalar()
        return category

    def get_categories(self) -> list[Category]:
        query = select(Category)
        with self.db_session() as session:
            category = session.execute(query).scalars().all()
        return category

    def create_category(self, category: CategorySchema) -> CategorySchema:
        category_model_alchemy = Category(id=category.id, type=category.type, name=category.name)
        with self.db_session() as session:
            session.add(category_model_alchemy)
            session.commit()
        return category

    def patch_category(self, category_id: int, name: str) -> Category:
        query = update(Category).where(Category.id == category_id).values(name=name).returning(Category)
        with self.db_session() as session:
            session.execute(query)
            session.commit()
        return self.get_category(category_id)

    def delete_category(self, category_id: int) -> None:
        query = delete(Category).where(Category.id == category_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()
