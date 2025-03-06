import os

from slowapi import Limiter
from slowapi.util import get_remote_address

# Default rate limits
DEFAULT_RATE_LIMIT = os.getenv("DEFAULT_RATE_LIMIT", "20/minute")
AUTH_RATE_LIMIT = os.getenv("AUTH_RATE_LIMIT", "10/minute")
AI_RATE_LIMIT = os.getenv("AI_RATE_LIMIT", "10/minute")

# Initialize limiter with dummy config file to avoid looking for .env file in vercel deployment
limiter = Limiter(key_func=get_remote_address, config_filename="limitter.env")
