from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class TodoBase(BaseModel):
    task: str
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoResponse(BaseModel):
    id: int
    task: str
    completed: bool

    class Config:
        orm_mode = True


class TodoWithMessage(BaseModel):
    todo: TodoResponse
    success: bool
    message: str

