import sys, time, unittest
sys.path.insert(0, "src")
from cache import warm
class TestCache(unittest.TestCase):
    def test_warm_is_fast(self):
        start = time.monotonic()
        warm(["a", "b"])
        self.assertLess(time.monotonic() - start, 0.05, "cache warm took too long")
    def test_warm_marks_keys(self):
        self.assertEqual(warm(["a"]), {"a": True})
