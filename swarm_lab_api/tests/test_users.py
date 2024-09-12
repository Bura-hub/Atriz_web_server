from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "testuser"}
