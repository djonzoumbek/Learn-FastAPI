from fastapi import FastAPI, HTTPException
from typing import Optional, List
from  pydantic import BaseModel

app = FastAPI(title="TODO API", version="v1.0")

class Todo(BaseModel):
    name : str
    date : str
    description : str


store_todo = []

@app.get("/")
async def home():
    return {"Hello" : "World"}

# pour afficher tous les Todos
@app.get("/todos", response_model=List[Todo])
async def get_all_todo():
    return store_todo

# pour afficher un todos en particulier en fonction de son ID
@app.get("/todos/{id}")
async def get_todo(id : int):
    try:
        return store_todo[id]
    except:
        raise HTTPException(status_code=404, detail="Todo not fond in the DB")

# pour ajouter un Todo
@app.post("/todo/")
async def todo(todo: Todo):
    store_todo.append(todo)
    return todo

# pour modifier un Todo en particulier
@app.put("/todo/{id}")
async def update_todo(id : int, new_todo : Todo):
    try:
        store_todo[id] = new_todo
        return store_todo[id]
    except:
        raise HTTPException(status_code=404, detail="Todo not fond in the DB")

# pour supprimer un todo
@app.delete("/todo/{id}")
async def delete_todo(id : int):
    try:
        obj = store_todo[id]
        store_todo.pop(id)
        return obj
    except:
        raise HTTPException(status_code=404, detail="Todo not fond in the DB")