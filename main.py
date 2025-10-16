from dotenv import load_dotenv
load_dotenv("dotenv.env")

import os
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from datetime import datetime, timedelta


from database import engine, session_local, get_db
from models import Base, Todo
from schemas import TodoCreate, TodoResponse, TodoWithMessage


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/todos/", response_model=TodoWithMessage, tags=["Qdo List🧾"])
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(task=todo.task)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    response = TodoWithMessage(
        todo=TodoResponse(id=db_todo.id, task=db_todo.task, completed=db_todo.completed),
        success=True,
        message="You created successfully"
    )

    return jsonable_encoder(response)


@app.get("/todos/", response_model=List[TodoResponse], tags=["Qdo List🧾"])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos


@app.put("/todos/{todo_id}", response_model=TodoResponse, tags=["Qdo List🧾"])
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="To-Do not found")
    db_todo.task = todo.task
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete("/todos/{todo_id}", response_model=TodoResponse, tags=["Qdo List🧾"])
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="To-Do not found")
    db.delete(db_todo)
    db.commit()
    return db_todo


@app.put("/todos/{todo_id}/complete", response_model=TodoResponse, tags=["Qdo List🧾"])
def toggle_todo_complete(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="To-Do not found")
    
    db_todo.completed = not db_todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo



