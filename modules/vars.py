import os

# Load Environment Variables
API_ID = int(os.getenv("API_ID", 123456))  # Replace with your actual API ID
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

PW_TOKEN = os.getenv("PW_TOKEN", "your_pw_token")  # Physics Wallah Token
PORT = int(os.getenv("PORT", 8080))  # Render requires PORT

# Download Folder
DOWNLOAD_PATH = "downloads"
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)