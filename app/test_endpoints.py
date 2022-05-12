from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)



def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

def test_post_home():
    response = client.post("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"message": "Hello World"}
