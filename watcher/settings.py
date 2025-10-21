import os
from dotenv import load_dotenv

load_dotenv()

# Telegram settings
API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH", "")
SESSION = os.getenv("TG_SESSION", "tg_session")

# Database
DB_PATH = os.getenv("DB_PATH", "data.sqlite")

# API Server
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")



