import sys, unittest
sys.path.insert(0, "src")
import payments
class TestPayments(unittest.TestCase):
    def test_config_has_token(self):
        self.assertTrue(payments.client_config()["token"])
