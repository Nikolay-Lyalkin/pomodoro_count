from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    access_token: str


class UserLoginOrCreate(BaseModel):
    username: str
    password: str
