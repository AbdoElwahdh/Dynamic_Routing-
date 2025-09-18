import time
from config import CACHE_ENABLED


class Cache:
    def __init__(self):
        self.cache = {}
        self.enabled = CACHE_ENABLED

    def get(self, key):
        if not self.enabled:
            return None

        if key in self.cache:
            entry = self.cache[key]
            return entry['value']

        return None

    def set(self, key, value):
        if not self.enabled:
            return
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }

    def clear(self):
        self.cache = {}
