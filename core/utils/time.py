import datetime
from  pytz import timezone

def get_ua_time():
    return datetime.datetime.now(tz=timezone("Europe/Helsinki"))