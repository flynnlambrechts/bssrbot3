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

def checkForDino(message):
    global day_value
    global week
    #global column
    global row
    global page
    global entity, value
    entity, value = wit_response(message)
    global response
    response = ""
    
    global current_day
    current_day = datetime.now(TIMEZONE).weekday()
    time = datetime.now(TIMEZONE).time().hour
    day = "Today"
    
    #See if user is asking about tomorrow
    if "tomorrow" in message or "tmrw" in message or "tomoz" in message:
        day = "Tomorrow"
        current_day+=1
        time = 0
        reponse = response + "Tomorrow"
        ## this will need to be changed to either go to next page or say that the menu hasnt been updated
        if current_day==7:
            if week==4:
                #response = response + "Sorry, I do not have the menu for next week yet!"
                return response
                week = 1
                print(str(week) + "week")
                column = 1
            else:
                week = week + 1
                print(str(week) + "week")
                column = 1
    if checkForDay(message):
        print("day found")
        week_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        if current_day > int(checkForDay(message)):
            week = week + 1
            day = str(week_days[int(checkForDay(message))])
            current_day = int(checkForDay(message))
        else:
            current_day = int(checkForDay(message))
            day = str(week_days[int(checkForDay(message))])
    #handling if meal is non-specified
    if value == "dino" or "cooking good looking" in message:
        if time < 10:
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
            response = response + "No more meals today :)"
    elif value == "breakfast":
        response = response + (f"Breakfast {day}: \n")
        day_value = current_day + 1
        response = response + breakfastmenu()
        
    elif value == "lunch":
        response = response + (f"Lunch {day}: \n")
        day_value = current_day + 1
        response = response + lunchmenu()

    elif value == "dinner":
        response = response + (f"Dinner {day}: \n")
        day_value = current_day + 1
        response = response + dinnermenu()
    return response

def breakfastmenu():
    global day_value
    global column
    global Range
    global page
    page = str((2*(week-1)+1))
    Range = int("2")
    response = ""
    for i in range(0,Range):
        try:
            header = ""
            column = 0
            header = header + columnlist()[i]
            content = ""
            if day_value == 8:
                column = 1
            else:
                column = day_value
            content = content + columnlist()[i]
            if content != "":
                response = response + str(header).title() + ": \n" + str(content).capitalize() + "\n\n"
        except IndexError:
            print('NOK')
    return response

def lunchmenu():
    global day_value
    global column
    global Range
    global page
    page = str((2*(week-1)+1.5))
    Range = int("2")
    response = ""
    for i in range(0,Range):
        try:
            header = ""
            column = 0
            header = header + columnlist()[i]
            content = ""
            if day_value == 8:
                column = 1
            else:
                column = day_value
            content = content + columnlist()[i]
            if content != "":
                response = response + str(header).title() + ": \n" + str(content).capitalize() + "\n\n"
        except IndexError:
            print('NOK')
    return response

def dinnermenu():
    global day_value
    global column
    global Range
    global page
    page = str((2*(week-1)+2))
    Range = int("7")
    response = ""
    for i in range(1,Range):
        try:
            header = ""
            column = 0
            header = header + columnlist()[i]
            content = ""
            if day_value == 8:
                column = 1
            else:
                column = day_value
            content = content + columnlist()[i]
            if content != "":
                response = response + str(header).title() + ": \n" + str(content).capitalize() + "\n\n"
        except IndexError:
            print('NOK')
    return response


def columnlist():
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

    
    info = []
    for td in menu_table_data[row].find_all("td"):
        if td is not None:
            plain_text = str(td).replace(r"– \n \n","- ").replace(r" \n \n", ", ").replace(r"– \n", "- ").replace(r"\n–","-").replace(", \n",", ").replace(r" \n ","").replace(r" \n",", ").replace(r"\n",", ")
            info.append(plain_text.replace("<td>","").replace("</td>","").replace("amp;",""))
        else:
            print("none!")
    #print(str(row) + str(column) + "row column")
    #print(info[column])
    return info[column]


