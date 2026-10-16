import random, time
def warm(keys):
    """Warm the cache. Network jitter is simulated with a random delay."""
    time.sleep(random.uniform(0.00, 0.08))
    return {k: True for k in keys}
