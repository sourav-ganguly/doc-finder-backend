import inspect
from functools import wraps

from fastapi import Request

from .rate_limit import (
    ADMIN_RATE_LIMIT,
    AI_RATE_LIMIT,
    AUTH_RATE_LIMIT,
    DEFAULT_RATE_LIMIT,
    limiter,
)


def rate_limit(limit_string=None):
    """
    Decorator to apply rate limiting to a route.

    Args:
        limit_string: Rate limit string (e.g. "10/minute"). If None, uses DEFAULT_RATE_LIMIT.
    """

    def decorator(func):
        limit = limit_string or DEFAULT_RATE_LIMIT
        is_async = inspect.iscoroutinefunction(func)

        @limiter.limit(limit)
        @wraps(func)
        async def async_wrapper(request: Request, *args, **kwargs):
            return await func(request, *args, **kwargs)

        @limiter.limit(limit)
        @wraps(func)
        def sync_wrapper(request: Request, *args, **kwargs):
            return func(request, *args, **kwargs)

        return async_wrapper if is_async else sync_wrapper

    return decorator


def auth_rate_limit():
    return rate_limit(AUTH_RATE_LIMIT)


def ai_rate_limit():
    return rate_limit(AI_RATE_LIMIT)


def doctor_rate_limit():
    return rate_limit(DEFAULT_RATE_LIMIT)


def admin_rate_limit():
    return rate_limit(ADMIN_RATE_LIMIT)
