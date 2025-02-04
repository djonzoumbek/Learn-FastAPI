import uvicorn
from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Optional
app = FastAPI()


class CoordIn(BaseModel):
    password : str
    lat: float
    lon: float
    zoom: Optional[int] = None
    description : Optional[str] = None

class CoordOut(BaseModel):
    lat: float
    lon: float
    zoom: Optional[int] = None
    description : Optional[str] = None




#
# @app.get("/")
# async def hello():
#     return {"message": "Hello World"}
#
#
# @app.get("/component/{component_id}") # path parameter
# async def get_component(component_id: int):
#     return {"component_id": component_id}


@app.get("/component/") # pour avoir plusieurs parametres. pour les paramettre obtionnneles on importe optional et on l'utilise
async def read_component(number : int, text: str):
    return {"number": number, "text": text}

@app.post("/position/", response_model=CoordOut, response_model_exclude={"description"})
async def make_position(coord: CoordIn ):
    return  coord #{"new_record": coord.dict()}



@app.post("/login/")
async def login(username : str = Form(...), password : str = Form(...)):
    return {username : username}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)