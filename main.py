from fastapi import FastAPI, HTTPException
from models import Todo, Todo_Pydantic, TodoIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, RegisterTortoise, register_tortoise
from pydantic import BaseModel

class Message(BaseModel):
    message : str

app = FastAPI()

# Create new Todos
@app.post("/todo", response_model=Todo_Pydantic)
async def create(todo : TodoIn_Pydantic):
    obj = await Todo.create(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_tortoise_orm(obj)
# Get one Todo
@app.get("/todo/{id}", response_model=TodoIn_Pydantic, responses={404 : {"model": HTTPNotFoundError}})
async def get_one(id : int):
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=id))

# Get Todos
@app.get("/todos")
async def todos():
    return await Todo_Pydantic.from_queryset(Todo.all())

# update
@app.put("/todo/{id}", response_model=Todo_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_todo(id: int, todo: TodoIn_Pydantic):
    updated_count = await Todo.filter(id=id).update(**todo.dict(exclude_unset=True))

    if not updated_count:
        raise HTTPException(status_code=404, detail="Todo not found")

    return await Todo_Pydantic.from_queryset_single(Todo.get(id=id))


#Delete

@app.delete("/delete/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_todo(id : int):
    delete_obj = await Todo.filter(id=id)
    if not delete_obj:
        raise HTTPException(status_code=404, detail="This to is not fond..")
    return Message(message="Successfull deleted !")


# make a connexion with sqlite db
register_tortoise(
    app,
    db_url="sqlite://store.db",
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)