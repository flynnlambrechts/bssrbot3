from datetime import *
import time
import calendar
import pytz
import datetime
TIMEZONE = pytz.timezone('Australia/Sydney')

numbers = [40,36,32,28,24,20,16,12,8,4]

x = datetime.datetime.now()

week = 35 #(int(x.strftime("%W"))-15)
'''
if week > 4:
        week = week - 4
'''
print(print(str(week) + " week"))

for i in numbers:
        print(i)
        if week > i:
                week = week - i
                print(str(week) + "week")
                break
        else:
                print("Nah")


