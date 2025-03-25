import time
from typing import Any

# In-memory cache store: user_id -> (timestamp, cached_data)
_cache = {}

CACHE_TTL = 300  # 5 minutes


def get_from_cache(key: Any):
    """Retrieve value from cache if not expired."""
    entry = _cache.get(key)
    if entry:
        timestamp, value = entry
        if time.time() - timestamp < CACHE_TTL:
            return value
        else:
            del _cache[key]
    return None


def set_cache(key: Any, value: Any):
    """Store value in cache with current timestamp."""
    _cache[key] = (time.time(), value)


def invalidate_cache(key: Any):
    """Remove value from cache."""
    _cache.pop(key, None)
