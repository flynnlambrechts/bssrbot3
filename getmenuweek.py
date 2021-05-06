import pytz
import datetime
TIMEZONE = pytz.timezone('Australia/Sydney')

numbers = [40,36,32,28,24,20,16,12,8,4]

x = datetime.datetime.now()
global week
week = (int(x.strftime("%W"))-15)
'''
if week > 4:
        week = week - 4
'''
print(print(str(week) + " week"))
def getmenuweek():
    global week
    menuweek = 0
    for i in numbers:
            print(i)
            if week > i:
                    menuweek = week - i
                    print(str(menuweek) + "week")
                    break
            else:
                    print("Nah")
                    menuweek = week
    return menuweek

print(getmenuweek())
