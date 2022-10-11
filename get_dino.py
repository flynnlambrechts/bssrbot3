#TheScrape3
from datetime import *

from killswitch import read_custom_message
from bot_constants import (week_days, Staff_ID, TIMEZONE)
from bot_functions import (PrintException, daysuntil)
from meal import Meal

#GLOSSARY:
#day_number: day of week 0-6 inclusive
#day_name: name of the day e.g. monday, wednesday, tomorrow, today
#week: week of cycle (1-4)

class Week:
	def __init__(self):
		self.number = getmenuweek()
	def add_one(self):
		if self.number==4:
			self.number = 1
			print(str(self.number) + " week")
		else:
			self.number += 1
			print(str(self.number) + "week")

	def add_weeks(self, n):
		self.number = (self.number + n)%4
		if self.number == 0: self.number = 4

def getmenuweek(): #1-4 inclusive cycle
	x = datetime.now(TIMEZONE)
	week = (int(x.strftime("%W"))+3) #plus one changes the cycle to match the dino cycle
	menuweek = (week)%4+1 #this cheeky +1 changes range from (0-3 to 1-4)
	print(str(menuweek) + " Menu Week")
	return menuweek


def getDino(message, value, recipient_id, con=None):
	try:
		time = datetime.now(TIMEZONE).time().hour
		week = Week()

		day_name, day_number, week = getDay(message, week)

		if value == "dino":
			if day_name == "Tomorrow":
				meal = Meal('breakfast')
			elif time < 10:
				meal  = Meal('breakfast')
			elif time < 14:
				meal = Meal('lunch')
			elif time < 19:
				meal = Meal('dinner')
			else: #after 7pm
				day_name, day_number, week = isTomorrow(day_name, day_number, week)
				meal = Meal('breakfast')

		elif value == "breakfast":
			if time > 14 and day_name == "Today": #after 2pm will give the breakfast for the next day
				day_name, day_number, week = isTomorrow(day_name, day_number, week)
			meal = Meal('breakfast')

		elif value == "lunch":
			if time > 17 and day_name == "Today": #after 5pm will give the lunch for the next day
				day_name, day_number, week = isTomorrow(day_name, day_number, week)
			meal = Meal('lunch')

		elif value == "dinner":
			if time > 21 and day_name == "Today":
				day_name, day_number, week = isTomorrow(day_name, day_number, week)
			meal = Meal('dinner')

		response = meal.getresponse(day_name, day_number, week.number)

		if con is not None:
			note = addnote(con, meal.name, day_name, recipient_id)
			if note is not None:
				response += str(note)

		#COUNT DOWN TO SPECIFIC EVENT
		# if day == "Today":
		# 	future = date(2021, 10, 18)
		# 	if date.today() <= future:
		# 		if recipient_id not in Staff_ID:
		# 			response = " ".join([response, "Happy freedom day!"])
		# 		else:
		# 			print("Staff")
		# 			#response = " ".join([response, str(daysuntil(future)), ""])
			else:
				print(False)
		return {'text': response, 'day': day_name, 'meal': meal.name}
	except:
		PrintException()
	



def getDay(message, week): #here is where we get the day and day_number and sometimes week
	#column = ""

	day_number = datetime.now(TIMEZONE).weekday()
	day_name = "Today"
	
	#See if user is asking about tomorrow
	if "tomorrow" in message or "tmrw" in message or "tomoz" in message or "tmoz" in message:
		day_name, day_number, week = isTomorrow(day_name, day_number, week)

	#check if user has asked about a day of the week
	elif checkForDay(message):
		print("Day Found!")
		day_number_requested = int(checkForDay(message))
		if day_number > day_number_requested:
			week.add_one()
		day_number = day_number_requested
		day_name = str(week_days[day_number])
	#otherwise must be today: and day and day_number are not updated from todays value
	return day_name, day_number, week

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

def isTomorrow(day_name, day_number, week):
	day_name = "Tomorrow"
	day_number+=1
	time = 0
	if day_number==7: #if after sunday
		week.add_one()
		day_number = 0 #sets it back to monday
	return day_name, day_number, week
	


def addnote(con, meal, day_name, recipient_id):
	note = None
	if day_name == "Today" and recipient_id not in Staff_ID: #makes sure we are talking about the actual day e.g. not tommorrow or the coming wednesday
		try: 
			note = "".join([u"Note: \uE301 \n",read_custom_message(meal, con),"\n\n"])
		except TypeError:
			#PrintException()
			print("Type Error in addnote: Probably no message.")
			pass
		except:
			PrintException()
	return note
