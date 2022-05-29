# FASTAPI Microservice to Extract Text from Images
Python &amp; FastAPI Tutorial: Create an ai microservice to extract text from images

### Objective

Learn how to deploy an AI microservice REST API endpoint using FastAPI, pytesseract, streamlit cloud Platform

### Streamlit deployment

Checkout the application [live here 🚀](https://share.streamlit.io/kshitijzutshi/fast-api-text-ocr/streamlit/streamlit.py)

**Screenshot 📸**

![image](https://user-images.githubusercontent.com/13203059/170846671-720807ae-0eee-43cd-bfe9-d5ad4cd661ad.png)


### Project Implementation Outline

 - Setup Requirements.txt
 - Setup Environment
 - Setup FastAPI App
 - FastAPI & Jinja Templates
 - FastAPI & PyTest
 - FastAPI Git & pre-commit
 - Deploy to DigitalOcean
 - Deploy Docker App to DigitalOcean App Platform
 - FastAPI Settings & Environment Variables & dotenv
 - Handling File Uploads
 - Automated Testing File Uploads
 - Image Upload Validation & Tests
 - Implementing Tesseract & pytesseract
 - Authorization Headers
 - Production Endpoint & Authorization Tests
 - One-Click Deploy on DigitalOcean App Platform

### Project Requirements

```
fastapi
gunicorn
uvicorn
jinja2
pytest
requests
pre-commit
python-dotenv
python-multipart
aiofiles
pillow

```

### Working with Pre-Commit

1. First, pip install pre-commit
2. Make a .pre-commit-config.yaml file
3. In the Terminal use : pre-commit-install
4. Next run the following command : pre-commit run --all-files

### Working with PyTest

1. Install pytest using pip
2. add pytest.ini file to exclude the directories pytest looks for testing code
3. Using pytest -s to stdout the test responses from endpoints as well.

### Working with Tesseract OCR

Reference - [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract)

[Check the PyPi package here](https://pypi.org/project/pytesseract/)

Use following command to install wrapper class for Google Tesseract OCR Engine:

```
pip install pytesseract

```

1. Install tesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki

2. Note the tesseract path from the installation. Default installation path at the time of this edit was: C:\Users\USER\AppData\Local\Tesseract-OCR. It may change so please check the installation path.

3. pip install pytesseract

4. Set the tesseract path in the script before calling image_to_string:

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'

### Securing the Endpoint using Auth Tokens

1. Generate a random token using Python secrets library

```
import secrets

secrets.token_urlsafe(32)

```

2. Save the generated tokens in a .env file