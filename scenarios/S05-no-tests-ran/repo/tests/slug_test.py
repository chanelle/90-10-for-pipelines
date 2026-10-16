import sys, unittest
sys.path.insert(0, "src")
from slug import slugify
class TestSlug(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Hello, World"), "hello-world")
