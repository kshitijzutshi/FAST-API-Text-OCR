from fastapi import FastAPI, Request, Response, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import pathlib
import os
import io
import uuid


BASE_DIR = pathlib.Path(__file__).parent
# create directory if dosent exist
if not os.path.exists(BASE_DIR / "uploads"):
    os.mkdir(BASE_DIR / "uploads")
UPLOADED_DIR = BASE_DIR / "uploads"

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Now we dont want to return a a JSON message instead
# retrun a HTML template using JinJa2
@app.get("/", response_class=HTMLResponse)
def home_view(request: Request):
    print(request)
    return templates.TemplateResponse("home.html", {"request": request, "title": "Kshitij"})

@app.post("/")
def home_detail_view():
    return {"message": "Hello World"}

@app.post("/img-echo", response_class=FileResponse)
async def img_echo_view(file: UploadFile = File(...)):
    bytes_str = io.BytesIO(await file.read())
    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    dest = UPLOADED_DIR / f"{uuid.uuid4()}{fext}"
    with open(dest, "wb") as f:
        f.write(bytes_str.read())
    return dest
