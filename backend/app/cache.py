"""简单的内存缓存，用于 API 响应"""

import time
import threading


class MemoryCache:
    def __init__(self):
        self._store: dict[str, tuple[float, object]] = {}
        self._lock = threading.Lock()

    def get(self, key: str):
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            expires_at, value = entry
            if time.time() > expires_at:
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: object, ttl: int = 300):
        with self._lock:
            self._store[key] = (time.time() + ttl, value)


_cache_instance = None


def get_cache() -> MemoryCache:
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = MemoryCache()
    return _cache_instance


def generate_cache_key(path: str) -> str:
    return f"cache:{path}"
