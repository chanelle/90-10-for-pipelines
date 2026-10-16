import sys, unittest
sys.path.insert(0, "src")
from uploads import is_png
class TestUploads(unittest.TestCase):
    def test_png(self):
        self.assertTrue(is_png(b"\x89PNG\r\n\x1a\n" + b"0" * 16))
