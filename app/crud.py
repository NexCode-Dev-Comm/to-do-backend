from sqlalchemy.orm import Session
from . import models, schemas  

def get_todos(db: Session):
    return db.query(models.Todo).all()

def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(task=todo.task)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
