__version__ = "2.0.0"
from datetime import datetime
def parse_datetime(s):
    return datetime.fromisoformat(s)
