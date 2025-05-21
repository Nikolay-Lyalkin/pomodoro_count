from pydantic import BaseModel, model_validator


class TaskSchema(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int

    class Config:

        from_attributes = True


    @model_validator(mode="after")
    def check_name_or_pomodoro_not_none(self):
        if not self.name and not self.pomodoro_count:
            raise ValueError("name or pomodoro must be provided")
        return self

