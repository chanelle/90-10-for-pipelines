import sys, unittest
sys.path.insert(0, "src")
import settings
class TestSettings(unittest.TestCase):
    def test_a_override_region(self):
        settings.set("region", "eu-west")
        self.assertEqual(settings.get("region"), "eu-west")
    def test_b_default_region(self):
        self.assertEqual(settings.get("region", "us-east"), "us-east")
