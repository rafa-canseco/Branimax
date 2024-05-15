from datetime import datetime
import pytz

TIMEZONE = "Etc/GMT+6"  # GMT-6

def to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.UTC)
    else:
        dt = dt.astimezone(pytz.UTC)
    return dt

def to_local(dt: datetime) -> datetime:
    local_tz = pytz.timezone(TIMEZONE)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.UTC)
    return dt.astimezone(local_tz)