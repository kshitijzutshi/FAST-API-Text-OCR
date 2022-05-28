import pathlib
import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kshitij\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
BASE_DIR = pathlib.Path(__file__).parent
IMG_DIR = BASE_DIR / "images"
img_1 = IMG_DIR / "ingredients-1.png"

img = Image.open(img_1)

preds = pytesseract.image_to_string(img)

preds_list = [x for x in preds.split("\n")]

print(preds_list)
