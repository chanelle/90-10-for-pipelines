import time
def report_date(epoch_seconds):
    """Business date for a timestamp. Uses the machine's local time zone."""
    return time.strftime("%Y-%m-%d", time.localtime(epoch_seconds))
