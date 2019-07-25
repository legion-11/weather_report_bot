from datetime import datetime

import pytz

hours = 18
minutes = 00

local = pytz.timezone("Europe/Kiev")
now = datetime.now(local)
notification_datetime = now.replace(hour=int(hours), minute=int(minutes), second=0)
if now > notification_datetime:
    notification_datetime = notification_datetime.replace(day=now.day + 1)
print(now)
print(notification_datetime)

print(now - notification_datetime)
delta = notification_datetime - now
print(now - delta)
print(now + delta)
