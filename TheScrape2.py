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

'''
global week
week = 1 ### work out how to define the week
'''

global column
column = 6

global page
page = str(7)

'''
def get_PageDayMeal(value):
    if value == "breakfast":
        page = str((2*(week-1)+1)
    elif value == "lunch" or "dinner":
        page = str(week + 1)
'''

def checkForDino(message):
    global week
    week = 1
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
    if "tomorrow" in message:
        day = "Tomorrow"
        current_day+=1
        time = 0
        reponse = response + "Tomorrow"
        ## this will need to be changed to either go to next page or say that the menu hasnt been updated
        if current_day==7:
            if week==4:
                response = response + "Sorry, I do not have the menu for next week yet!"
                return response
            else:
                week = week + 1
                print(str(week) + "week")
                column = 1
            
    
    #handling if meal is non-specified
    if value == "dino": #or "cooking good looking" in message:
        if time < 10:
            response = response + (f"{day}'s breakfast is:")
            '''
            page = str((2*(week-1)+1))
            column = current_day
            row = 0
            response = str(response) + "\n1" + str(getinfo())
            '''
            #response = response + (todayMenu.breakfast)
        elif time < 14:
            response = response + (f"{day}'s lunch is:")
            #response = response + (str(todayMenu.lunch))
        elif time < 19:
            response = response + (f"{day}'s dinner is:")
            #response = response + (str(todayMenu.dinner))
        else: 
            response = response + "No more meals today :)"
    elif value == "breakfast":
        response = response + (f"{day}'s breakfast is:")
        page = str((2*(week-1)+1))
        print(page + " page")
        day_value = current_day + 1
        print(str(day_value) + "day value")
        row = 0
        if day_value == 8:
            column = 1
        else:
            column = day_value
        print(str(column) + " column1")
        print(str(row) + " row1")
        response = str(response) + "\n" + str(getinfo(column))
    elif value == "lunch":
        response = response + (f"{day}'s lunch is:")
        page = str((2*(week-1)+1.5))
        print(page + " page")
        day_value = current_day + 1
        print(str(day_value) + "day value")
        if day_value == 8:
            column = 1
        else:
            column = day_value
        response = response + lunchmenu()
        '''
        page = str(2*week)
        print(page + " page")
        day_value = current_day + 1
        print(str(day_value) + "day value")
        
        row = 2
        '''
        
    elif value == "dinner":
        response = response + (f"{day}'s dinner is:")
        #response = response + (str(todayMenu.dinner))
    return response


def lunchmenu():
    global row
    response = ""
    for i in range(0,4):
        print(i)
        row = i
        response = response + RowHearders(i)[i] + getinfo(column)[i]
    return response

def RowHeaders(i):
    headers = []
    column=0
    headers.append(getinfo(column))
    return headers


def getinfo(column):
    global page
    
    ################## # Opening the html file
    HTMLFile = open(str(page + ".html"), "r") #try putting in func.

    # Reading the file
    index = HTMLFile.read()
      
    # Creating a BeautifulSoup object and specifying the parser
    soup = BeautifulSoup(index, 'lxml')

    # Using the prettify method to modify the code
    #print(soup.body.prettify())

    #print(soup.title) #prints the table title if it has one

    menu_table = soup.find("table", attrs={"class": "dataframe"})
    menu_table_data = menu_table.tbody.find_all("tr")  # contains 2 rows
    ##################

    
    info = []
    for td in menu_table_data[row].find_all("td"):
        if td is not None:
            plain_text = str(td).replace(r" \n \n", ", ").replace(r"– \n", "- ").replace(r"\n–","-").replace(", \n",", ").replace(r" \n ","").replace(r" \n",", ").replace(r"\n",", ") + "."
            info.append(plain_text.replace("<td>","").replace("</td>","").replace("amp;",""))
        else:
            print("none!")
    print(str(row) + str(column) + "row column")
    print(info[column])
    return info


