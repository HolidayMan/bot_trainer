from datetime import datetime, timedelta
from datetime import timezone as dttz
from pytz import timezone

utc_ua_offset = datetime.now(dttz.utc).astimezone().utcoffset() // timedelta(hours=1)

def get_ua_time():
    return datetime.now(tz=timezone("Europe/Helsinki"))

OCLOCK_8 = timedelta(hours=6) + timedelta(hours=utc_ua_offset)
