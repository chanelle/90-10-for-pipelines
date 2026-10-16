_CACHE = {}
def get(key, default=None):
    return _CACHE.get(key, default)
def set(key, value):
    _CACHE[key] = value
