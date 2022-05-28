from fastapi import FastAPI, Request, Header, Response, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import pathlib
import os
import io
import uuid
from PIL import Image
import pytesseract
import dotenv

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kshitij\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

BASE_DIR = pathlib.Path(__file__).parent
# create directory if dosent exist
if not os.path.exists(BASE_DIR / "uploads"):
    os.mkdir(BASE_DIR / "uploads")
UPLOADED_DIR = BASE_DIR / "uploads"

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

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


# Now we dont want to return a a JSON message instead
# retrun a HTML template using JinJa2
@app.get("/", response_class=HTMLResponse)
def home_view(request: Request):
    print(request)
    return templates.TemplateResponse("home.html", {"request": request, "title": "Kshitij"})

# @app.post("/")
# def home_detail_view():
#     return {"message": "Hello World"}
@app.post("/", response_class=FileResponse)
async def img_prediction_view(file: UploadFile = File(...), authorization = Header(None)):
    # Verify the auth token
    verify_auth(authorization)
    # read the file upload as a byte string
    print(await file.read())
    bytes_str = io.BytesIO(await file.read())
    print(bytes_str)
    try:
        # read the byte string as an image
        image = Image.open(bytes_str)
    except:
        raise HTTPException(status_code=400, detail="Invalid image")
    preds = pytesseract.image_to_string(image)
    preds_list = [x for x in preds.split("\n")]
    return {"results": preds_list, "original": preds}


@app.post("/img-echo/", response_class=FileResponse)
async def img_echo_view(file: UploadFile = File(...), authorization = Header(None)):
    # verify the auth token
    verify_auth(authorization)
    # read the file upload as a byte string
    bytes_str = io.BytesIO(await file.read())
    try:
        # read the byte string as an image
        image = Image.open(bytes_str)
    except:
        raise HTTPException(status_code=400, detail="Invalid image")
    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    dest = UPLOADED_DIR / f"{uuid.uuid4()}{fext}"
    # with open(dest, "wb") as f:
    #     f.write(bytes_str.read())
    image.save(dest)
    return dest
