from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import databases
import sqlalchemy
from datetime import datetime

DATABASE_URL = "sqlite:///./db_test.db"

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)

# Définition de la table register
register = sqlalchemy.Table(
    "register",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(140)),
    sqlalchemy.Column("date_created", sqlalchemy.DateTime(), default=datetime.utcnow)
)

# Création de l'engine pour SQLAlchemy
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Création de la base de données (synchrone, donc pas besoin d'async)
metadata.create_all(engine)

app = FastAPI()

# Connexion à la base de données
@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()

# Modèle Pydantic pour la réponse
class Register(BaseModel):
    id: int
    name: str
    date_created: datetime

# Modèle Pydantic pour l'entrée
class RegisterIn(BaseModel):
    name: str = Field(...)

# Route pour créer un enregistrement
@app.post("/register/", response_model=Register)
async def create(r: RegisterIn = Depends()):
    query = register.insert().values(
        name=r.name,
        date_created=datetime.utcnow()
    )

    record_id = await database.execute(query)

    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)

    return Register(**row)

@app.get("/register/{id}", response_model=Register)
async def get_one(id : int):
    query = register.select().where(register.c.id == id)
    user = await database.fetch_one(query)

    return {**user}

@app.get("/register/", response_model=List[Register])
async def get_all():
    query = register.select()
    all_get = await database.fetch_all(query)
    return all_get

@app.put("/register/{id}", response_model=Register)
async def update(id: int, r: RegisterIn = Depends()):
    query = register.update().where(register.c.id == id).values(
        name = r.name,
        date_created = datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.delete("/register/{id}", response_model = Register)
async def delete(id :int):
    query = register.delete().where(register.c.id == id)
    return  await database.execute(query)