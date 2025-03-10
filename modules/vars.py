import os

# Load Environment Variables
API_ID = int(os.getenv("API_ID", 25513009))  # Replace with your actual API ID
API_HASH = os.getenv("API_HASH", "33ace9b0779df4387a8ad8b7fbe6b050")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7855125251:AAEFxHuBgS6JTJFBSNYvCmR9Mjw--_tNJoA")

PW_TOKEN = os.getenv("PW_TOKEN", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDE5NDI1MDkuMTA0LCJkYXRhIjp7Il9pZCI6IjYxM2I2MThkOGU2NGE2MDAxMTU5ZjE5MCIsInVzZXJuYW1lIjoiOTY2NDExNDQ3NyIsImZpcnN0TmFtZSI6Imtlc2hhdiIsImxhc3ROYW1lIjoiIiwib3JnYW5pemF0aW9uIjp7Il9pZCI6IjVlYjM5M2VlOTVmYWI3NDY4YTc5ZDE4OSIsIndlYnNpdGUiOiJwaHlzaWNzd2FsbGFoLmNvbSIsIm5hbWUiOiJQaHlzaWNzd2FsbGFoIn0sImVtYWlsIjoia2VzaGF2Y2hvdWRoYXJ5NDcyM0BnbWFpbC5jb20iLCJyb2xlcyI6WyI1YjI3YmQ5NjU4NDJmOTUwYTc3OGM2ZWYiXSwiY291bnRyeUdyb3VwIjoiSU4iLCJ0eXBlIjoiVVNFUiJ9LCJpYXQiOjE3NDEzMzc3MDl9.o18jD-CC_iIv67MugFn2NJW8KcMQ8Lu2Zc9VIzy4Cnk")  # Physics Wallah Token
PORT = int(os.getenv("PORT", 8080))  # Render requires PORT

# Download Folder
DOWNLOAD_PATH = "downloads"
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)