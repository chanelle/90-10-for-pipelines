import sys, unittest
sys.path.insert(0, "src")
from orders import subtotal, apply_discount
class TestOrders(unittest.TestCase):
    def test_subtotal(self):
        self.assertEqual(subtotal([(2, 5)]), 10)
    def test_discount(self):
        self.assertEqual(apply_discount(100, 10), 90)
