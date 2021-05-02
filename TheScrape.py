from datetime import *
import time
import calendar
import pytz
TIMEZONE = pytz.timezone('Australia/Sydney')

# Importing BeautifulSoup class from the bs4 module
from bs4 import BeautifulSoup
import requests

from app import value

week = int(1) ### work out how to define the week

row = 0
column = 1
page = str(1)

'''
def get_PageDayMeal(value):
    if value == "breakfast":
        page = str((2*(week-1)+1)
    elif value == "lunch" or "dinner":
        page = str(week + 1)
'''

def checkForDino(message):
    response = ""
    global current_day
    current_day = datetime.now(TIMEZONE).weekday()
    time = datetime.now(TIMEZONE).time().hour
    day = "Today"
    
    #See if user is asking about tomorrow
    if "tomorrow" in message:
        day = "Tomorrow"
        current_day+=1
        time = 0
        reponse = response + "Tomorrow"
        ## this may need be to changed depending on how big the menu is 
        if current_day==7:
            response = response + "Sorry, do not have the menu for next week yet!"
            return response
        
    #todayMenu = getDayMenu(current_day)
    
    #handling if meal is non-specified
    if value == "dino": #or "cooking good looking" in message:
        if time < 10:
            response = response + (f"{day} breakfast is:")
            page = str((2*(week-1)+1))
            column = current_day
            row = 0
            reponse = reponse + "\n1" + getinfo
            #response = response + (todayMenu.breakfast)
        elif time < 14:
            response = response + (f"{day} lunch is:")
            #response = response + (str(todayMenu.lunch))
        elif time < 19:
            response = response + (f"{day} dinner is:")
            #response = response + (str(todayMenu.dinner))
        else: 
            response = response + "No more meals today :)"
    elif value == "breakfast":
        response = response + (f"{day} breakfast is:")
        #response = response + (todayMenu.breakfast)
    elif value == "lunch":
        response = response + (f"{day} lunch is:")
        #response = response + (str(todayMenu.lunch))
    elif value == "dinner":
        response = response + (f"{day} dinner is:")
        #response = response + (str(todayMenu.dinner))
    return response


# Opening the html file
HTMLFile = open(str(page + ".html"), "r")
  
# Reading the file
index = HTMLFile.read()
  
# Creating a BeautifulSoup object and specifying the parser
soup = BeautifulSoup(index, 'lxml')

# Using the prettify method to modify the code
#print(soup.body.prettify())

#print(soup.title) #prints the table title if it has one

menu_table = soup.find("table", attrs={"class": "dataframe"})
menu_table_data = menu_table.tbody.find_all("tr")  # contains 2 rows

# Get all the headings of Lists

def getinfo():
    info = []
    for td in menu_table_data[row].find_all("td"):
        if td is not None:
            # remove any newlines and extra spaces from left and right
            #headings.append(td.b.text.replace('\n', ' ').strip())
            info.append(td)
        else:
            print("none!")
    print(info[column])
    return info[column]


