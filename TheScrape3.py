#TheScrape3
from datetime import *
import time

from pytz import timezone
from bs4 import BeautifulSoup # Importing BeautifulSoup class from the bs4 module

from killswitch import read_custom_message
from bot_constants import (week_days, Staff_ID)
from bot_functions import (PrintException, daysuntil)


TIMEZONE = timezone('Australia/Sydney')

#GLOSSARY:
#current_day: day of week 0-6 inclusive
#daynumber:  day of week 0-6 inclusive represents day user asked for
#day: name of the day e.g. monday, wednesday, tomorrow, today
#week: week of cycle (1-4)

class Meal:
	def __init__(self, week, meal=None, day=None):
		self.week = getmenuweek() #week defaults to current week of cycle
		self.Range = range(0,1)
		self.page = 0
		self.headers = ["Header1","Header2","Header3"]

	def getresponse(self ,value, day, current_day, week):
		mealname = type(self).__name__
		x = 0
		self.response = f"{mealname} {day}: \n".title()
		column = current_day + 1
		column_list = columnlist(self.page, column, self.Range)

		for i in self.Range:
			if i == 5: #skips if it's the vegetables row
				x += 1
				continue
			try:
				content = ""
				content = content + column_list[i]
				#print(str(i) + " " + content)
				if content != "":
					content = addemojiscontent(content)
					self.response = "".join([self.response, self.headers[x],": \n",str(content).capitalize(),"\n\n"])
				else:
					print("Blank content: " + self.headers[x])
				x += 1

			except IndexError:
				print('NOK ' + str(i))
		return self.response

class Breakfast(Meal):
	def __init__(self, week, meal=None, day=None):
		self.Range = range(0,2)
		self.page = str((2*(week-1)+1))
		self.headers = [u"Residential Breakfast \U0001f95e", "Special"]

class Lunch(Meal):
	def __init__(self, week, meal=None, day=None):
		self.Range = range(1,3)
		self.page = str((2*(week-1)+1.5))
		self.headers = [u"Hot Option \U0001F37D", u"Vegetarian Option \U0001F331", u"Salad \U0001F957"]#u"Soup \U0001f372"]

class Dinner(Meal):
	def __init__(self, week, meal=None, day=None):
		self.Range = range(2,8)
		self.page = str((2*(week-1)+2))
		self.headers = [u"Main Course \U0001F37D", u"Vegetarian \U0001F331", u"Salad \U0001F957", "Vegetables", u"Additional Vegetables \U0001F966", u"The Dessert Station \U0001f370"]


def getDino(message, value, recipient_id, con=None):
	try:
		time = datetime.now(TIMEZONE).time().hour
		week = getmenuweek()

		day, current_day, week = getDay(message, week)

		if value == "dino":
			if day == "Tomorrow":
				meal = Breakfast(week)
			elif time < 10:
				meal  = Breakfast(week)
			elif time < 14:
				meal = Lunch(week)
			elif time < 19:
				meal = Dinner(week)
			else: #after 7pm
				day, current_day, week = isTomorrow(day, current_day, week)
				meal = Breakfast(week)

		elif value == "breakfast":
			if time > 14 and day == "Today": #after 2pm will give the breakfast for the next day
				day, current_day, week = isTomorrow(day, current_day, week)
			meal = Breakfast(week)

		elif value == "lunch":
			if time > 17 and day == "Today": #after 5pm will give the lunch for the next day
				day, current_day, week = isTomorrow(day, current_day, week)
			meal = Lunch(week)

		elif value == "dinner":
			if time > 21 and day == "Today":
				day, current_day, week = isTomorrow(day, current_day, week)
			meal = Dinner(week)

		response = meal.getresponse(value, day, current_day, week)

		if con is not None:
			note = addnote(con, meal, day, recipient_id)
			if note is not None:
				response = response + str(note)

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
		return response
	except:
		PrintException()
	

def getmenuweek(): #1-4 inclusive cycle
	x = datetime.now(TIMEZONE)
	week = (int(x.strftime("%W"))+3) #plus three changes the cycle to match the dino cycle
	menuweek = (week)%4+1 #this cheeky +1 changes range from (0-3 to 1-4)
	print(str(menuweek) + " Menu Week")
	return menuweek

def getDay(message, week): #here is where we get the day and current_day and sometimes week
	#column = ""

	current_day = datetime.now(TIMEZONE).weekday()
	day = "Today"
	
	#See if user is asking about tomorrow
	if "tomorrow" in message or "tmrw" in message or "tomoz" in message or "tmoz" in message:
		day, current_day, week = isTomorrow(day, current_day, week)

	#check if user has asked about a day of the week
	elif checkForDay(message):
		print("Day Found!")
		daynumber = int(checkForDay(message))
		if current_day > daynumber:
			print(str(week) + " week, checkForDay")
			if str(week)==str("4"):
				week = 1
				print(str(week) + " week, checkForDay if 4")
			else:
				week = week + 1
				print(str(week) + " week, checkForDay else")
		current_day = daynumber
		day = str(week_days[current_day])
	#otherwise must be today: and day and current_day are not updated from todays value
	return day, current_day, week

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

def isTomorrow(day, current_day, week):
	day = "Tomorrow"
	current_day+=1
	time = 0
	if current_day==7: #if after sunday
		if week==4:
			week = 1
			print(str(week) + " week")
		else:
			week = week + 1
			print(str(week) + "week")
		current_day = 0 #sets it back to monday
	return day, current_day, week
	

def addemojiscontent(content):
	#content = content.replace("egg", u"egg \U0001F95A")
	content = content.replace("pancakes", u"pancakes \U0001f95e")
	content = content.replace("pizza", u"pizza \U0001f355")
	content = content.replace("sushi", u"sushi \U0001f363")
	content = content.replace("chicken", u"chicken \U0001F357")
	#content = content.replace("honey", u"honey \U0001F36F")
	return content


def columnlist(page, column, Range): #gets the info from each column as a list
	rowcontents = []
	menu_table_data = openhtml(page)
	for i in range(0,Range[-1]+1): #still includes the first two rows for dinner
		row = i
		content = getinfo(menu_table_data, row, column)
		rowcontents.append(content)
	return rowcontents

def addnote(con, meal, day, recipient_id):
	meal = type(meal).__name__.lower()
	note = None
	if day == "Today" and recipient_id not in Staff_ID: #makes sure we are talking about the actual day e.g. not tommorrow or the coming wednesday
		try: 
			note = "".join([u"Note: \uE301 \n",read_custom_message(meal, con),"\n\n"])
		except TypeError:
			#PrintException()
			print("Type Error in addnote: Probably no message.")
			pass
		except:
			PrintException()
	return note

def openhtml(page):
#-----------------------Opening the HTML file--------------------------#
	HTMLFile = open(str("menu/" + page + ".html"), "r") #try putting in func.
	#print(str(HTMLFile))
	# Reading the file
	index = HTMLFile.read()
	  
	# Creating a BeautifulSoup object and specifying the parser
	soup = BeautifulSoup(index, 'lxml')

	# Using the prettify method to modify the code
	#print(soup.body.prettify())

	#print(soup.title) #prints the table title if it has one

	menu_table = soup.find("table", attrs={"class": "dataframe"})
	menu_table_data = menu_table.tbody.find_all("tr")  # contains 2 rows
#---------------------------------------------------------------------#
	return menu_table_data

def getinfo(menu_table_data, row, column): #this is where the scraping happens
	info = []
	for td in menu_table_data[row].find_all("td"):
		if td is not None:
			#plain_text = str(td).replace(r"– \n \n","- ").replace(r" \n \n", ", ").replace(r"– \n", "- ").replace(r"\n–","-").replace(", \n",", ").replace(r" \n ","").replace(r" \n",", ").replace(r"\n",", ")
			stuff = str(td).replace("<td>","").replace("</td>","").replace("amp;","").replace(r"\n","")
			#plain_text  =  stuff.strip(""",.;:-¢"'�_!?I•,L4J£<~""") #removes all weird artifacts
			info.append(stuff)
		else:
			print("none!")
	return info[column]



