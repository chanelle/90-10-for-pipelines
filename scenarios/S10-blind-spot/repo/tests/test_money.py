import sys, unittest
sys.path.insert(0, "src")
from money import round_currency
class TestMoney(unittest.TestCase):
    def test_round_currency_runs(self):
        round_currency(2.675)  # executes the line, asserts nothing
