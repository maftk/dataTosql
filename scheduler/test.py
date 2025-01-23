import jpholiday
import datetime
today = datetime.datetime.now()
print(today)
isholiday = jpholiday.is_holiday(today.date())
print(isholiday)
