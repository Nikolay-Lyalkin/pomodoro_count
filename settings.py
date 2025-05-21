from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    name_db: str = 'pomodoro.sqlite'
