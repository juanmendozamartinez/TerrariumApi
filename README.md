
# FastAPI Raspberry Pi Camera Server

This project sets up a FastAPI server on a Raspberry Pi, allowing the server to capture images using the Raspberry Pi camera, upload them to Google Drive, and return them via an API endpoint. The image storage path is configurable via environment variables, ensuring flexibility for different setups.

## Features
- **Capture Images**: Uses the Raspberry Pi camera to capture images.
- **Upload to Google Drive**: Images are automatically uploaded to Google Drive.
- **API Security**: API endpoint is secured with an API key.
- **Environment Variables**: Sensitive information (like paths and credentials) is stored in environment variables for easy configuration.

## Requirements
Before setting up the server, ensure you have the following installed on your Raspberry Pi:
- **Python 3.x** (preferably Python 3.7 or newer)
- **FastAPI**: Web framework for building APIs.
- **uvicorn**: ASGI server for running FastAPI apps.
- **google-auth**, **google-auth-oauthlib**, and **google-auth-httplib2**: Required for Google Drive API authentication.
- **libcamera**: To interface with the Raspberry Pi camera module.
- **python-dotenv** (optional): To manage environment variables from a `.env` file.

## Installation

### 1. Set Up Your Raspberry Pi
Ensure your Raspberry Pi is set up with:
- Raspberry Pi OS installed.
- SSH enabled for remote access.
- Camera module connected and enabled (`sudo raspi-config` > Interface Options > Camera).

### 2. Install Required Packages
Start by updating your Raspberry Pi:
```bash
sudo apt-get update && sudo apt-get upgrade
```

Install Python dependencies:
```bash
sudo apt-get install python3-pip
pip3 install fastapi uvicorn google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

### 3. Enable and Test the Camera
If you haven't already enabled the camera, do so using:
```bash
sudo raspi-config
```
Then, test the camera using:
```bash
libcamera-still -o test.jpg
```

### 4. Set Up Google Drive API
Follow [this guide](https://developers.google.com/drive/api/v3/quickstart/python) to create a Google Cloud project, enable the Google Drive API, and download the credentials JSON file.

### 5. Create Environment Variables
Set up the environment variables for sensitive data like API keys and Google Drive credentials.

Edit `~/.bashrc` or create a `.env` file in the project directory:
```bash
export API_KEY="your_secret_api_key"
export DRIVE_CREDENTIALS_PATH="/path/to/credentials.json"
export IMAGE_PATH="/home/pi/images"
```
Then, source the `.bashrc` or load the `.env` file:
```bash
source ~/.bashrc
```

Alternatively, create a `.env` file in the project directory with:
```bash
API_KEY="your_secret_api_key"
DRIVE_CREDENTIALS_PATH="/path/to/credentials.json"
IMAGE_PATH="/home/pi/images"
```

### 6. Run the FastAPI Server

Run the FastAPI server using `uvicorn`:
```bash
uvicorn terrariumApi:app --host 0.0.0.0 --port 8000 --reload
```
The server will now be accessible at `http://<raspberry_pi_ip>:8000`.

### 7. Test the Camera Endpoint
You can test the camera endpoint by accessing it from your browser or via a tool like `curl`:
```bash
curl -X 'GET' 'http://<raspberry_pi_ip>:8000/camera/?api_key=your_secret_api_key'
```

### 8. Secure the Server (Optional)
For production use, ensure the API is behind a firewall, use HTTPS for secure communication, and store API keys securely.

## File Structure

```
.
├── terrariumApi.py         # FastAPI server
├── .env                    # Environment variables file (optional)
├── token.pickle            # Google Drive OAuth token (generated after the first use)
└── requirements.txt        # Python dependencies
```

## Configuration

You can modify the following environment variables:
- **API_KEY**: Your custom API key for securing the `/camera/` endpoint.
- **DRIVE_CREDENTIALS_PATH**: The path to your Google Drive API credentials JSON file.
- **IMAGE_PATH**: The directory where images will be saved. Default is `/tmp/images/`.

## Notes
- **Google Drive API**: The first time you access the `/camera/` endpoint, the app will prompt you to authenticate with Google. This is handled by `InstalledAppFlow` and the token will be saved in `token.pickle`.
- **Image Storage**: The `IMAGE_PATH` should be an existing directory where images will be stored before being uploaded to Google Drive.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

