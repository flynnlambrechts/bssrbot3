import pytz
import datetime
TIMEZONE = pytz.timezone('Australia/Sydney')

#multiples of 4 to account for the four week cycle (must be less than 40)
numbers = [40,36,32,28,24,20,16,12,8,4]

x = datetime.datetime.now(TIMEZONE)
global week
#15 is value from the current week of the year to the start of the current menu
week = (int(x.strftime("%W"))-15)

#print(print(str(week) + " week"))
def getmenuweek():
    global week
    menuweek = 0
    for i in numbers:
            #print(i)
            if week > i:
                    menuweek = week - i
                    #print(str(menuweek) + "week")
                    break
            else:
                    #print("Nah")
                    menuweek = week
    return menuweek

#print(getmenuweek())
