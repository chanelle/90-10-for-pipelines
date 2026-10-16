import fastparse
def event_day(s):
    return fastparse.parse_date(s).date().isoformat()
