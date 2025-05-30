from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from database.models import User
from exceptions import UserNotFound
from schemas.user import UserSchema
from service.user_service import UserService


class UserRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user(self, user_id: int) -> UserSchema:
        query = select(User).where(User.id == user_id)
        with self.db_session as session:
            user = session.execute(query).scalars().one_or_none()

        return UserSchema(id=user.id, access_token=user.access_token)

    def create_user(self, username: str, password: str) -> UserSchema:
        query = insert(User).values(username=username,
                                    password=password).returning(User.id)
        with self.db_session as session:
            user_id: int = session.execute(query).scalar()
            access_token = UserService.generate_access_token(user_id)
            session.execute(
                update(User).where(User.username == username, User.password == password).values(
                    access_token=access_token))
            session.commit()
        return self.get_user(user_id)

    def login_user(self, username: str, password: str) -> UserSchema:
        query = select(User).where(User.username == username, User.password == password)
        with self.db_session as session:
            user = session.execute(query).scalars().one_or_none()
        if user:
            return user
        if not user:
            raise UserNotFound
