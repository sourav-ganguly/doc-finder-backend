from functools import wraps

from fastapi import Request

from .rate_limit import AI_RATE_LIMIT, AUTH_RATE_LIMIT, DEFAULT_RATE_LIMIT, limiter


def rate_limit(limit_string=None):
    """
    Decorator to apply rate limiting to a route.

    Args:
        limit_string: Rate limit string (e.g. "10/minute"). If None, uses DEFAULT_RATE_LIMIT.
    """

    def decorator(func):
        limit = limit_string or DEFAULT_RATE_LIMIT

        @limiter.limit(limit)
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator


# Predefined rate limiters for common endpoints
def auth_rate_limit():
    return rate_limit(AUTH_RATE_LIMIT)


def ai_rate_limit():
    return rate_limit(AI_RATE_LIMIT)
