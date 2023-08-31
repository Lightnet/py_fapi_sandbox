from datetime import datetime
from sqlalchemy import String, DateTime, TIMESTAMP
now = datetime.now()
print("now:", now)
print("now.timestamp():", now.timestamp())
timestamp = int(now.timestamp())
print("timestamp: ",timestamp)

print("TIMESTAMP: ",TIMESTAMP)