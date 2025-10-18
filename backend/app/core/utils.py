import datetime

def utc_now():
    return datetime.datetime.now(tz=datetime.UTC)
