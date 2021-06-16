import pytz
import datetime
TIMEZONE = pytz.timezone('Australia/Sydney')

#multiples of 4 to account for the four week cycle (must be less than 40)
numbers = [40,36,32,28,24,20,16,12,8,4]



#print(print(str(week) + " week"))
def getmenuweek():
    x = datetime.datetime.now(TIMEZONE)
    global week
    #15 is value from the current week of the year to the start of the current menu
    week = (int(x.strftime("%W"))-14) #21 to 22
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
    print(str(menuweek) + "week -1")
    #menuweek = 4
    return menuweek

#print(getmenuweek())


def checkForDay(message): #check of day of week specified
    day = "" 
    if "monday" in message or " mon" in message or "mon " in message:
        day = str('0')
    elif "tuesday" in message or " tues" in message or "tues " in message:
        day = 1
    elif "wednesday" in message or " wed" in message or "wed " in message:
        day = 2 
    elif "thursday" in message or " thur" in message or "thur " in message or " thurs" in message or "thurs " in message:
        day = 3
    elif "friday" in message or " fri" in message or "fri " in message:
        day = 4
    elif "saturday" in message or " sat" in message or "sat " in message:
        day = 5
    elif "sunday" in message or " sun" in message or "sun " in message:
        day = 6
    return day
