from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pathlib


BASE_DIR = pathlib.Path(__file__).parent

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
