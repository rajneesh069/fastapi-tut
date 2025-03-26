from enum import IntEnum
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

app = FastAPI()


class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1


class TodoBase(BaseModel):
    title: str = Field(
        ..., min_length=3, max_length=150, description="Title of the todo"
    )
    description: str = Field(
        ..., min_length=5, max_length=512, description="Description of the todo"
    )
    priority: Priority = Field(
        default=Priority.LOW, description="Priority of the task/todo."
    )


class Todo(TodoBase):
    id: UUID = Field(default=uuid4(), description="Unique ID of the todo")


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(
        None, min_length=3, max_length=150, description="Title of the todo"
    )
    description: Optional[str] = Field(
        None, min_length=5, max_length=512, description="Description of the todo"
    )
    priority: Optional[Priority] = Field(
        default=None, description="Priority of the task/todo."
    )


all_todos: List[Todo] = [
    Todo(title="Go to gym", description="Go to gym at 1700", priority=Priority.HIGH),
    Todo(
        title="Buy groceries",
        description="Milk, Bread, and Eggs",
        priority=Priority.HIGH,
    ),
    Todo(
        title="Read a book",
        description="Finish reading the Python tutorial",
        priority=Priority.HIGH,
    ),
    Todo(
        title="Call mom",
        description="Catch up with mom over the phone",
        priority=Priority.HIGH,
    ),
    Todo(
        title="Write a blog post",
        description="Share Python tips on your blog",
        priority=Priority.MEDIUM,
    ),
    Todo(
        title="Plan weekend trip",
        description="Organize a weekend getaway with friends",
        priority=Priority.LOW,
    ),
]


@app.get("/", response_model=None)
def index():
    return {"message": "The server is working!"}


@app.get("/todos", response_model=List[Todo])
def get_todos(
    first_n: int = None,
):  # first_n is a query param if it is NOT specified as a path param
    if first_n is not None:
        return all_todos[:first_n]
    else:
        return all_todos


@app.get("/todos/{id}", response_model=Todo, status_code=200)
def get_todo(id: UUID):
    for todo in all_todos:
        if id == todo.id:
            return todo

    raise HTTPException(404, detail="Todo not found")


@app.post("/todos", response_model=Todo, status_code=201)
def add_todo(
    todo: TodoBase,
):  # here "todo" is the request body expected in this POST route
    new_todo = Todo(**todo.model_dump())  # create a Todo from todobase
    all_todos.append(new_todo)
    return new_todo


@app.put("/todos/{id}", response_model=Todo)
def update_todo(id: UUID, new_todo: TodoUpdate):
    for existing_todo in all_todos:
        if id == existing_todo.id:
            existing_todo.title = new_todo.title or existing_todo.title
            existing_todo.description = (
                new_todo.description or existing_todo.description
            )
            existing_todo.priority = new_todo.priority or existing_todo.priority
            return existing_todo
    raise HTTPException(status_code=404, detail="Todo not found.")


@app.delete("/todos/{id}", response_model=Todo)
def delete_todo(id: UUID):
    for index, todo in enumerate(all_todos):
        if todo.id == id:
            deleted_todo = all_todos.pop(index)
            return deleted_todo

    raise HTTPException(status_code=404, detail="Todo not found.")
