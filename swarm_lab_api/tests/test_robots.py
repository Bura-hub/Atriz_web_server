from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_robot():
    response = client.get("/robots/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Robot", "type": "Type A"}
