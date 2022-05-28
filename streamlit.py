import pandas as pd
import requests
import streamlit as st
import os
import pathlib
from fastapi import FastAPI, Request, Header, Response, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import io
import uuid
from PIL import Image
import pytesseract
import dotenv
import base64
import json

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kshitij\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

BASE_DIR = pathlib.Path(__file__).parent
# create directory if dosent exist
if not os.path.exists(BASE_DIR / "uploads"):
    os.mkdir(BASE_DIR / "uploads")
UPLOADED_DIR = BASE_DIR / "uploads"

app = FastAPI()

# read the app auth token from env file
dotenv.load_dotenv()
AUTH_TOKEN = os.getenv("APP_AUTH_TOKEN")
AUTH_TOKEN_PROD = os.getenv("APP_AUTH_TOKEN_PROD")



def verify_auth(authorization = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    label, token = authorization.split()
    if token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authorization token")


@app.post("/", response_class=FileResponse)
async def img_prediction_view(file: UploadFile = File(...), authorization = Header(None)):
    # Verify the auth token
    verify_auth(authorization)
    # read the file upload as a byte string
    print(await file.read())
    # bytes_str = io.BytesIO(await file.read())
    # print(bytes_str)
    try:
        # read the byte string as an image
        image = Image.open(file)
    except:
        raise HTTPException(status_code=400, detail="Invalid image")
    preds = pytesseract.image_to_string(image)
    preds_list = [x for x in preds.split("\n")]
    return {"results": preds_list, "original": preds}


st.set_page_config(layout="wide")
st.title(":camera: Image Text Extraction app")


# Let user upload a picture
with st.sidebar:
    st.title("Upload a picture")

    upload_type = st.radio(
        label="How to upload the picture",
        options=(("From file", "From URL", "From webcam")),
    )

    image_bytes = None

    if upload_type == "From file":
        file = st.file_uploader(
            "Upload image file", type=[".png"], accept_multiple_files=False
        )
        if file:
            image_bytes = file.getvalue()

    # if upload_type == "From URL":
    #     url = st.text_input("Paste URL")
    #     if url:
    #         image_bytes = requests.get(url).content

    # if upload_type == "From webcam":
    #     camera = st.camera_input("Take a picture!")
    #     if camera:
    #         image_bytes = camera.getvalue()

st.write("## Uploaded picture")
if image_bytes:
    st.write("🎉 Here's what you uploaded!")
    st.write(file.name)
    st.image(image_bytes, width=200)
else:
    st.warning("👈 Please upload an image first...")
    st.stop()


st.write("## Extracted Text")

# Extract text from the image
if image_bytes:
    st.write("🎉 Here's what we extracted from the picture!")
    st.write(pytesseract.image_to_string(Image.open(file)))
