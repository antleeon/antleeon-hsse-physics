import datetime

def now_milliseconds_since_month():
    curr = datetime.datetime.now()
    curr_ms = ((((((curr.day * 24) + curr.hour) * 60) + curr.minute) * 60) + curr.second) * 1000 + (curr.microsecond / 1000)
    return curr_ms