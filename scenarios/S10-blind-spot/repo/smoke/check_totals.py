import sys
sys.path.insert(0, "src")
from money import round_currency
got = round_currency(2.675)
print(f"round_currency(2.675) = {got}; expected 2.68 (half-up, per pricing policy)")
sys.exit(0 if got == 2.68 else 1)
