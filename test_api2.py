from fastapi.testclient import TestClient
from api2 import app

client = TestClient(app)

def read_root():
    response = client.get("/")
    assert response.status_code == 201
    assert response.json() == {"message" : "message"}