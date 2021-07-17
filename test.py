import datetime
from pytz import timezone
TIMEZONE = timezone('Australia/Sydney')

def daysuntil(day): #date provided in date(YYYY,M,D) format
    today = date.today()
    diff = day - today
    return (diff.days)

# day = date(2021,9,13)
# print(daysuntil(day))

# day = date(2021, 9, 13)
# if date.today() <= day:
# 	print(True)
# else:
# 	print(False)


# current_day = datetime.now(TIMEZONE).weekday()
# print(current_day.date())

row = "2021-07-17 07:57:57.759856"
time = datetime.datetime.strptime(row, '%Y-%m-%d %H:%M:%S.%f')
time = time.strftime('%I:%M%p %d %b')
print(time)