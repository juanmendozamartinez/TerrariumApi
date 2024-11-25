import subprocess
import random
import os
import time
import io
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader

# Load environment variables
from dotenv import load_dotenv

load_dotenv()  # Automatically load variables from .env if used

app = FastAPI()

# Environment variables
API_KEY = os.getenv("API_KEY")
DRIVE_CREDENTIALS_PATH = os.getenv("DRIVE_CREDENTIALS_PATH")
IMAGE_DIR = os.getenv("IMAGE_PATH", "/tmp/images/")  # Default if not set

# Middleware: Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Secure the endpoint with an API key
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

@app.get("/camera/", dependencies=[Depends(verify_api_key)])
async def capture_and_upload_image():
    # Check if the image directory exists, create if not
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    # Generate a unique image path with a random number
    random_number = random.randint(1000, 9999)
    image_path = os.path.join(IMAGE_DIR, f"captured_image_{random_number}.jpg")

    # Capture image using libcamera
    subprocess.run(["libcamera-still", "-t", "2000", "-o", image_path])

    # Wait for the image to be created
    while not os.path.exists(image_path):
        time.sleep(0.1)  # Check every 100ms

    # Upload image to Google Drive (you can implement this as per your needs)

    # Read the image file and return it as a response
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    return {
        "status": "Image captured and uploaded successfully",
        "image": StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")
    }
