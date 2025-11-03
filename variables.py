"""Environment variables loading module."""
import os
from dotenv import load_dotenv
from logger_config import setup_logger

# Load environment variables from .env file
load_dotenv()

logger = setup_logger(__name__)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# API Configuration
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))

# File Upload Configuration
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
ALLOWED_EXTENSIONS = os.getenv(
    "ALLOWED_EXTENSIONS", "jpg,jpeg,png,webp"
).split(",")

# Validate required configuration
if not OPENAI_API_KEY:
    error_msg = "OPENAI_API_KEY is required but not set in environment"
    logger.error(error_msg)
    raise ValueError(error_msg)

if not OPENAI_API_KEY.startswith("sk-"):
    logger.warning(
        "OPENAI_API_KEY does not start with 'sk-', "
        "please verify it is correct"
    )

logger.info("Configuration loaded successfully")
