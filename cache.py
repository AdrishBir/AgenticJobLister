class SimpleCache:
    """
    A simple in-memory cache to prevent redundant API calls.
    """
    def __init__(self):
        self.cache = {}

    async def get(self, key: str):
        return self.cache.get(key)

    async def set(self, key: str, value):
        self.cache[key] = value

# Global cache instance
cache = SimpleCache()
