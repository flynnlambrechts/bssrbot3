from datetime import *
import time
import calendar
import pytz
TIMEZONE = pytz.timezone('Australia/Sydney')

# Importing BeautifulSoup class from the bs4 module
from bs4 import BeautifulSoup
import requests

#from utils import value
from utils import wit_response
from getmenuweek import getmenuweek
from getmenuweek import checkForDay
'''
global week
week = 1 ### work out how to define the week
'''

global column
column = 6

global page
page = str(7)

global week
week = getmenuweek()
print(str(week) + " week thescrape2")


#define the dino times here used throughout
breakfasttime = "7:00-10:00am"
lunchtime = "12:15-2:15pm"
dinnertime = "5:00-7:15pm"
dinotimes = "Dino Times: \nBreakfast: " + breakfasttime + "\nLunch: " + lunchtime + "\nDinner: " + dinnertime



def checkForDino(message):
    global current_day #day of week 0-6 inclusive
    global day_value #day of week 1-7 inclusive
    global day #name of the day e.g. monday, wedneday, tomorrow, today
    global week #week of cycle
    week = getmenuweek()
    print(str(week) + " week checkfordino")
    global breakfasttime, lunchtime, dinnertime, dinotimes
    global entity, value
    entity, value = wit_response(message)
    #global response
    response = ""
    
    getDay(message) #checks for days
    
    #handling if meal is non-specified
    if value == "dino" or "cooking good looking" in message:
        time = datetime.now(TIMEZONE).time().hour
        if "time" in message:
            response = response + dinotimes
        elif day == "Tomorrow":
            response = response + (f"Dino Breakfast Tomorrow: \n")
            day_value = current_day + 1
            response = response + breakfastmenu()
        elif time < 10:
            response = response + (f"Breakfast {day}: \n")
            day_value = current_day + 1
            response = response + breakfastmenu()
            
        elif time < 14:
            response = response + (f"Lunch {day}: \n")
            day_value = current_day + 1
            response = response + lunchmenu()
        elif time < 19:
            response = response + (f"Dinner {day}: \n")
            day_value = current_day + 1
            response = response + dinnermenu()
        else: 
            response = response + (f"Breakfast Tomorrow: \n")
            day_value = current_day + 1
            response = response + breakfastmenu()
    elif value == "breakfast":
        if "time" in message:
            response = response + "Breakfast at dino is at " + breakfasttime 
        else:
            response = response + (f"Breakfast {day}: \n")
            day_value = current_day + 1
            response = response + breakfastmenu()
        
    elif value == "lunch":
        if "time" in message:
            response = response + "Lunch at dino is at " + lunchtime
        else:
            response = response + (f"Lunch {day}: \n")
            day_value = current_day + 1
            response = response + lunchmenu()

    elif value == "dinner":
        if "time" in message:
            response = response + "Dinner at dino is at " + dinnertime
        else:
            response = response + (f"Dinner {day}: \n")
            day_value = current_day + 1
            response = response + dinnermenu()
    if "time" not in message: #adds feedback link to end of response unless user is asking for time
        response = response + " \nPlease leave feedback here: https://bit.ly/3hVT0DX"
    return response

def getDay(message): #here is where we get the day and current_day and sometimes week
    global current_day
    global day
    global week
    global column
    print(str(week) + " week a")
    current_day = datetime.now(TIMEZONE).weekday()
    day = "Today"
    
    #See if user is asking about tomorrow
    if "tomorrow" in message or "tmrw" in message or "tomoz" in message:
        day = "Tomorrow"
        current_day+=1
        time = 0
        ## this will need to be changed to either go to next page or say that the menu hasnt been updated
        if current_day==7:
            if week==4:
                week = 1
                print(str(week) + " week")
                column = 1
            else:
                week = week + 1
                print(str(week) + "week")
                column = 1
    #check if user has asked about a day of the week
    elif checkForDay(message):
        print("day found")
        week_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        if current_day > int(checkForDay(message)):
            print(str(week) + " week")
            if str(week)==str("4"):
                week = 1
                print(str(week) + " week")
            else:
                week = week + 1
                print(str(week) + " week")
            current_day = int(checkForDay(message))
            day = str(week_days[int(checkForDay(message))])
        else:
            current_day = int(checkForDay(message))
            day = str(week_days[int(checkForDay(message))])

    #otherwise must be today: and day and current_day are not updated from todays value



def breakfastmenu():
    global day_value
    global column
    global Range
    global page
    global week
    page = str((2*(week-1)+1))
    Range = int("2")
    response = ""
    for i in range(0,Range):
        try:
            header = ""
            column = 0
            header = header + columnlist()[i]
            header = addemojis(header)
            content = ""
            if day_value == 8:
                column = 1
            else:
                column = day_value
            content = content + columnlist()[i]
            if content != "":
                content = addemojiscontent(content)
                response = response + str(header).title() + ": \n" + str(content).capitalize() + "\n\n"
        except IndexError:
            print('NOK')
    return response

def lunchmenu():
    global day_value
    global column
    global Range
    global page
    global week
    page = str((2*(week-1)+1.5))
    Range = int("3")
    response = ""
    for i in range(0,Range):
        try:
            header = ""
            column = 0
            header = header + columnlist()[i]
            header = addemojis(header)
            content = ""
            if day_value == 8:
                column = 1
            else:
                column = day_value
            content = content + columnlist()[i]
            if content != "":
                content = addemojiscontent(content)
                response = response + str(header).title() + ": \n" + str(content).capitalize() + "\n\n"
        except IndexError:
            print('NOK')
    return response

def dinnermenu():
    global day_value
    global column
    global Range
    global page
    global week
    page = str((2*(week-1)+2))
    Range = int("8")
    response = ""
    for i in range(1,Range):
        try:
            header = ""
            column = 0 #set to first column to get header
            header = header + columnlist()[i]
            header = addemojis(header)
            content = ""
            if day_value == 8:
                column = 1
            else:
                column = day_value
            content = content + columnlist()[i]
            if header == "vegetables":
                content = ""
            if content != "":
                content = addemojiscontent(content)
                response = response + str(header).title() + ": \n" + str(content).capitalize() + "\n\n"
        except IndexError:
            print('NOK')
    return response

def addemojis(header):
    header = header.replace("salad", u"salad \U0001F957")
    if "vegetarian option" in header:
        header = header.replace("vegetarian option", u"vegetarian option \U0001F331")
    else:
        header = header.replace("vegetarian", u"vegetarian \U0001F331")
    header = header.replace("main course", u"main course \U0001F37D").replace("hot option", u"hot option \U0001F37D")
    header = header.replace("residential breakfast", u"residential breakfast \U0001f95e")
    header = header.replace("soup", u"soup \U0001f372")
    header = header.replace("the dessert station", u"the dessert station \U0001f370")
    header = header.replace("additional vegetables", u"additional vegetables \U0001F966")
    return header

def addemojiscontent(content):
    #content = content.replace("egg", u"egg \U0001F95A")
    content = content.replace("pancake", u"pancake \U0001f95e")
    content = content.replace("pizza", u"pizza \U0001f355")
    content = content.replace("sushi", u"sushi \U0001f363")
    content = content.replace("chicken", u"chicken \U0001F357")
    content = content.replace("honey", u"honey \U0001F36F")
    return content

def columnlist(): #gets the info from each column as a list
    global row
    global column
    rowcontents = []
    for i in range(0,Range):
        row = i
        content = getinfo(column)
        rowcontents.append(content)
    return rowcontents


def getinfo(column):
    global page
    global row
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
    try:
        menu_table = soup.find("table", attrs={"class": "dataframe"})
        menu_table_data = menu_table.tbody.find_all("tr")  # contains 2 rows
    except AttributeError:
        menu_table = soup.find("table", attrs={"class": "t1"})
        menu_table_data = menu_table.tbody.find_all("tr")  # contains 2 rows
    #---------------------------------------------------------------------#
    info = []
    for td in menu_table_data[row].find_all("td"):
        if td is not None:
            #plain_text = str(td).replace(r"– \n \n","- ").replace(r" \n \n", ", ").replace(r"– \n", "- ").replace(r"\n–","-").replace(", \n",", ").replace(r" \n ","").replace(r" \n",", ").replace(r"\n",", ")
            stuff = str(td).replace("<td>","").replace("</td>","").replace("amp;","").replace(r"\n","")
            plain_text  =  stuff.strip(""",.;:-¢"'�_!?I•,L4J£<~""") #removes all weird artifacts
            info.append(plain_text)
        else:
            print("none!")
    #print(str(row) + str(column) + "row column")
    #print(info[column])
    return info[column]


