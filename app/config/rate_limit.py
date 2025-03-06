import os

from slowapi import Limiter
from slowapi.util import get_remote_address

# Default rate limits
DEFAULT_RATE_LIMIT = os.getenv("DEFAULT_RATE_LIMIT", "60/minute")
AUTH_RATE_LIMIT = os.getenv("AUTH_RATE_LIMIT", "10/minute")
AI_RATE_LIMIT = os.getenv("AI_RATE_LIMIT", "30/minute")

# Initialize limiter with Redis if available
limiter = Limiter(key_func=get_remote_address)

# REDIS_URL = os.getenv("REDIS_URL")
# if REDIS_URL:
#     print("Redis URL found")
#     # from slowapi.storage import RedisStorage

#     # storage = RedisStorage(REDIS_URL)
#     # limiter = Limiter(
#     #     key_func=get_remote_address, storage_uri=REDIS_URL, storage=storage
#     # )
# else:
#     # Use in-memory storage if Redis is not available
#     limiter = Limiter(key_func=get_remote_address)
