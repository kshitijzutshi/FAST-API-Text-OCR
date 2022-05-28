from http.client import HTTPException
from importlib.resources import path
from app.main import app, BASE_DIR, UPLOADED_DIR
from fastapi.testclient import TestClient
import shutil
from fastapi import Header
import time
import io
import os
from PIL import Image, ImageChops
import dotenv

"""
Use pytest -s to run all tests

"""

# read the app auth token from env file
dotenv.load_dotenv()
AUTH_TOKEN = os.getenv("APP_AUTH_TOKEN")
AUTH_TOKEN_PROD = os.getenv("APP_AUTH_TOKEN_PROD")

client = TestClient(app)

def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

# def test_post_home():
#     response = client.post("/")
#     assert response.status_code == 200
#     assert response.headers["content-type"] == "application/json"
#     assert response.json() == {"message": "Hello World"}
def test_invalid_file_upload_error():
    response = client.post("/") # requests.post("") # python requests
    assert response.status_code == 422
    assert  "application/json" in response.headers['content-type']

def test_echo_upload():
    img_saved_path = BASE_DIR / "images"
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None
        response = client.post("/img-echo/",
                    files={"file": open(path, 'rb')},
                    headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        if img is None:
            assert response.status_code == 400
        else:
            # Returning a valid image
            assert response.status_code == 200
            r_stream = io.BytesIO(response.content)
            echo_img = Image.open(r_stream)
            difference = ImageChops.difference(echo_img, img).getbbox()
            assert difference is None
    # time.sleep(3)
    shutil.rmtree(UPLOADED_DIR)

def test_prediction_upload():
    img_saved_path = os.path.join(BASE_DIR, "images")
    print(img_saved_path)
    # print(list(UPLOADED_DIR.glob("*")))
    # path = list((BASE_DIR / "uploads").glob("*"))[0]
    for path in os.listdir(img_saved_path):
        try:
            image = Image.open(path)
        except:
            image = None
        response = client.post("/",
                    files={"file": open(f'{img_saved_path}\\{path}', "rb")},
                    headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        # file_extension = str(path.suffix).replace(".", "")
        if image is None:
            assert response.status_code == 400
        else:
            # assert file_extension in response.headers["content-type"]
            print(response.status_code)
            assert response.status_code == 200
            data = response.json()
            # assert len(data.keys()) == 2
