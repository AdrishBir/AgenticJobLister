import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_ENDPOINT = os.getenv("OPENROUTER_ENDPOINT", "https://openrouter.ai/api/v1")

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")

# Scraper Configuration
SCRAPER_USER_AGENTS = os.getenv("SCRAPER_USER_AGENTS", "Mozilla/5.0 (Windows NT 10.0; Win64; x64),Chrome/91.0").split(",")

# Other configuration parameters
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))
LLM_MAX_RETRIES = int(os.getenv("LLM_MAX_RETRIES", 3))
