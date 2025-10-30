from pydantic import BaseModel


class TodoBase(BaseModel):
    task: str
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoResponse(BaseModel):
    id: int
    task: str
    completed: bool

    model_config = {
        "from_attributes": True  
    }


class TodoWithMessage(BaseModel):
    todo: TodoResponse
    success: bool
    message: str
