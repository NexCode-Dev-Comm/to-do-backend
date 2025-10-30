from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi.encoders import jsonable_encoder

from .. import schemas, crud
from ..database import get_db

router = APIRouter(
    prefix="/todos",
    tags=["To-do List🧾"]
)


@router.post("/", response_model=schemas.TodoWithMessage)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = crud.create_todo(db, todo)
    response = schemas.TodoWithMessage(
        todo=schemas.TodoResponse.from_orm(db_todo),
        success=True,
        message="To-Do created successfully"
    )
    return jsonable_encoder(response)


@router.get("/", response_model=List[schemas.TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)


@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id, todo)
    return db_todo


@router.delete("/{todo_id}", response_model=schemas.TodoWithMessage)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo(db, todo_id)
    return schemas.TodoWithMessage(
        todo=None,
        success=True,
        message="To-Do deleted successfully"
    )


@router.put("/{todo_id}/complete", response_model=schemas.TodoResponse)
def toggle_todo_complete(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.toggle_todo_complete(db, todo_id)
    return db_todo
