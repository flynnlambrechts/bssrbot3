from pytz import timezone
from datetime import datetime

TIMEZONE = timezone('Australia/Sydney')

def getmenuweek(): #1-4 inclusive cycle
	x = datetime.now(TIMEZONE)
	week = (int(x.strftime("%W"))+3) #plus one changes the cycle to match the dino cycle
	menuweek = (week)%4+1 #this cheeky +1 changes range from (0-3 to 1-4)
	print(str(menuweek) + " Menu Week")
	return menuweek

if __name__ == "__main__":
    print(f"The week is {getmenuweek()}.")