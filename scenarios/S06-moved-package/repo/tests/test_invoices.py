import unittest
from invoices import total
class TestInvoices(unittest.TestCase):
    def test_total(self):
        self.assertEqual(total([(2, 1.5), (1, 3.0)]), 6.0)
