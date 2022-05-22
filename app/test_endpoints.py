from importlib.resources import path
from app.main import app, BASE_DIR, UPLOADED_DIR
from fastapi.testclient import TestClient
import shutil
import time

"""
Use pytest -s to run all tests

"""

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

def test_echo_upload():
    img_saved_path = BASE_DIR / "images"
    # print(list(UPLOADED_DIR.glob("*")))
    # path = list((BASE_DIR / "uploads").glob("*"))[0]
    for path in img_saved_path.glob("*.png"):

        response = client.post("/img-echo", files={"file": open(path, "rb")})
        assert response.status_code == 200
        print(response.headers)
        assert response.headers["content-type"] == "image/png"
        # assert response.headers["content-disposition"] == "inline; filename=image.png"
        # assert response.headers["content-length"] == "15"
        # assert response.headers["content-transfer-encoding"] == "binary"
    # shutil.rmtree(UPLOADED_DIR)
    # time.sleep(3)