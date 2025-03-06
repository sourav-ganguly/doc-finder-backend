from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.config import Config

# Default rate limits
DEFAULT_RATE_LIMIT = "60/minute"
AUTH_RATE_LIMIT = "120/minute"
AI_RATE_LIMIT = "10/minute"

# Initialize limiter with empty config to avoid looking for .env file in vercel deployment
config = Config(environ={})
limiter = Limiter(key_func=get_remote_address, config=config)

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
