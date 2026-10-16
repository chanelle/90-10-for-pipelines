def refundable(order_total, days_since_purchase, policy_days=30):
    if days_since_purchase > policy_days:
        return 0.0
    if order_total <= 0:
        return 0.0
    fee = 0.05 * order_total if order_total > 100 else 0.0
    amount = order_total - fee
    if amount < 1:
        return 0.0
    return round(amount, 2)
def reason(days_since_purchase, policy_days=30):
    if days_since_purchase > policy_days:
        return "outside window"
    return "eligible"
