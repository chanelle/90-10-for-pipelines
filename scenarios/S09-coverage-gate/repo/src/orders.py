def subtotal(lines):
    return sum(q * p for q, p in lines)
def apply_discount(amount, pct):
    return amount * (1 - pct / 100)
