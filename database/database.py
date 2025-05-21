from sqlalchemy import create_engine
from settings import Settings
from sqlalchemy.orm import sessionmaker

settings = Settings()


engine = create_engine(f"postgresql+psycopg2://postgres:9998441653Qq@localhost/{settings.name_db}")
Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session
