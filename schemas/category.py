from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: int
    type: str
    name: str
