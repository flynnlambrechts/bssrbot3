from datetime import *
from pytz import timezone
TIMEZONE = timezone('Australia/Sydney')

def getmenuweek(): #1-4 inclusive cycle
	x = datetime.now(TIMEZONE)
	week = (int(x.strftime("%W"))+1) #plus three changes the cycle to match the dino cycle
	menuweek = (week)%4+1 #this cheeky +1 changes range from (0-3 to 1-4)
	print(str(menuweek) + " Menu Week")
	return menuweek

getmenuweek()