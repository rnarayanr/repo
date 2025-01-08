from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool =False

# In-memory database for tasks
tasks: List[Task] =[]

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    if any(existing_task.id == task.id for existing_task in tasks):
        raise HTTPException(status_code=400, detail='Task with this id exists already')
    tasks.append(task)

@app.put("/tasks/{task_id}", response_model=Task)
def edit_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return updated_task
        raise HTTPException(status_code=404, detail="task not found")

@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return tasks
