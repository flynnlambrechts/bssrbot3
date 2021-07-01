from datetime import *
import time
#import calendar
#import pytz
from pytz import timezone
TIMEZONE = timezone('Australia/Sydney')

# Importing BeautifulSoup class from the bs4 module
from bs4 import BeautifulSoup
import requests

#from utils import value
#from utils import wit_response
from getmenuweek import getmenuweek
from getmenuweek import checkForDay
from killswitch import read_custom_message
'''
global week
week = 1 ### work out how to define the week
'''

#global column
column = 6

#global page
page = str(7)

#global week
week = getmenuweek()
print(str(week) + " week thescrape2")


#define the dino times here used throughout
breakfasttime = "7:00-7:45am" #"7:00-10:00am"
lunchtime = "11:45-12:30pm" #"12:15-2:15pm"
dinnertime = "4:30-5:15pm"  #"5:00-7:15pm"
dinotimes = "".join(["Basser Dino Times: \nBreakfast: ", breakfasttime, "\nLunch: ", lunchtime, "\nDinner: ", dinnertime])



def checkForDino(message, con, value):
    print("checkForDino")
    #global current_day #day of week 0-6 inclusive
    #global day_value #day of week 1-7 inclusive
    #global day #name of the day e.g. monday, wedneday, tomorrow, today
    #global week #week of cycle
    week = getmenuweek()
    #print(str(week) + " week checkfordino")
    #global breakfasttime, lunchtime, dinnertime, dinotimes
    #global entity, value
    #entity, value = wit_response(message)
    response = ""
    
    day, current_day, column = getDay(message, week) #checks for days and creates current_day
    time = datetime.now(TIMEZONE).time().hour
    #handling if meal is non-specified
    if value == "dino": 
        #time = datetime.now(TIMEZONE).time().hour
        if "time" in message:
            response = response + dinotimes
        elif day == "Tomorrow":
            response = response + (f"Dino Breakfast Tomorrow: \n")
            day_value = current_day + 1
            print(current_day)
            print(day_value)
            response = response + breakfastmenu(day_value, column, week)
        elif time < 10:
            response = response + (f"Breakfast {day}: \n")
            day_value = current_day + 1
            response = response + breakfastmenu(day_value, column, week)
        elif time < 14:
            response = response + (f"Lunch {day}: \n")
            day_value = current_day + 1
            response = response + lunchmenu(day_value, column, week)
        elif time < 19:
            response = response + (f"Dinner {day}: \n")
            day_value = int(datetime.now(TIMEZONE).weekday()) + 1
            #day_value = current_day + 1 #maybe should be this?????
            response = response + dinnermenu(day_value, column, week)
        else: 
            response = response + (f"Breakfast Tomorrow: \n")
            day_value = int(datetime.now(TIMEZONE).weekday()) + 2 #this might have to be 1 but idk wth is going on
            print(current_day)
            print(day_value)
            response = response + breakfastmenu(day_value, column, week)
    elif value == "breakfast":
        if "time" in message:
            response = response + "Basser breakfast is at " + breakfasttime
        elif time > 14: #after 2pm will give the value for the next day
            day = "Tomorrow"
            response = response + (f"Breakfast {day}: \n")
            day_value = current_day + 2
            response = response + breakfastmenu(day_value, column, week)
        else:
            response = response + (f"Breakfast {day}: \n")
            day_value = current_day + 1
            response = response + breakfastmenu(day_value, column, week)
        
    elif value == "lunch":
        if "time" in message:
            response = response + "Basser lunch is at " + lunchtime
        elif time > 17: #after 2pm will give the value for the next day
            day = "Tomorrow"
            response = response + (f"Lunch {day}: \n")
            day_value = current_day + 2
            response = response + lunchmenu(day_value, column, week)
        else:
            response = response + (f"Lunch {day}: \n")
            day_value = current_day + 1
            response = response + lunchmenu(day_value, column, week)

    elif value == "dinner":
        if "time" in message:
            response = response + "Basser dinner is at " + dinnertime
        else:
            response = response + (f"Dinner {day}: \n")
            day_value = current_day + 1
            response = response + dinnermenu(day_value, column, week)
    #if "time" not in message: #adds feedback link to end of response unless user is asking for time
        #response = response + " \nPlease leave feedback here: https://bit.ly/3hVT0DX"
    note = addnote(con, value, day)
    if note is not None and "time" not in message:
        response = response + str(note)
    print("checkForDino DONE")
    return response

def checkForButton(message):
    print("checkForButton")
    if "time" not in message: #adds feedback link to end of response unless user is asking for time
        #response = response + " \nPlease leave feedback here: https://bit.ly/3hVT0DX"
        url_buttons = [{
                    "type": "web_url",
                    "url": "https://bit.ly/3hVT0DX",
                    "title": "Leave Feedback"
                    },
                    {
                    "type": "web_url",
                    "url": "https://user.resi.inloop.com.au/home",
                    "title": "Latemeal"
                    }
                    ]
    else:
        url_buttons = []
    print("checkForButton DONE")
    return url_buttons

def getDay(message, week): #here is where we get the day and current_day and sometimes week
    column = ""
    #print(str(week) + " week a")
    current_day = datetime.now(TIMEZONE).weekday()
    day = "Today"
    
    #See if user is asking about tomorrow
    if "tomorrow" in message or "tmrw" in message or "tomoz" in message or "tmoz" in message:
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
    #elif "today" in message:
        #day = "Today"
    return day, current_day, column

    #otherwise must be today: and day and current_day are not updated from todays value

# def wholedaymenu(message):
#     global day_value
#     global column
#     #global Range
#     global page
#     global week

#     day, current_day, week, column = getDay(message, week)
#     if day == "Today":
#         response = response + (f"Breakfast {day}: \n")
#         day_value = current_day + 1
#         response = response + breakfastmenu() + "\n\n"

#         response = response + (f"Lunch {day}: \n")
#         response = response + lunchmenu() + "\n\n"

#         response = response + (f"Dinner {day}: \n")
#         response = response + dinnermenu() + "\n\n"

#     elif day == "Tomorrow":
#     elif checkForDay(message):


def breakfastmenu(day_value, column, week):
    page = str((2*(week-1)+1))
    Range = int("2")
    response = ""
    for i in range(0,Range):
        try:
            header = ""
            column = 0
            header = header + columnlist(page, column, Range)[i]
            header = addemojis(header)
            content = ""
            if day_value == 8:
                column = 1
            else:
                column = day_value
            content = content + columnlist(page, column, Range)[i]
            if content != "":
                content = addemojiscontent(content)
                response = "".join([response,str(header).title(),": \n",str(content).capitalize(),"\n\n"])
        except IndexError:
            print('NOK')
    return response

def lunchmenu(day_value, column, week):
    page = str((2*(week-1)+1.5))
    Range = int("3")
    response = ""
    for i in range(0,Range):
        try:
            header = ""
            column = 0
            header = header + columnlist(page, column, Range)[i]
            header = addemojis(header)
            content = ""
            if day_value == 8:
                column = 1
            else:
                column = day_value
            content = content + columnlist(page, column, Range)[i]
            if content != "":
                content = addemojiscontent(content)
                response = "".join([response,str(header).title(),": \n",str(content).capitalize(),"\n\n"])
        except IndexError:
            print('NOK')
    return response

def dinnermenu(day_value, column, week):
    #print("dinnermenu")
    page = str((2*(week-1)+2))
    Range = int("8")
    response = ""
    for i in range(1,Range):
        try:
            header = ""
            column = 0 #set to first column to get header
            header = "".join([header,columnlist(page, column, Range)[i]])
            header = addemojis(header)
            content = ""
            if day_value == 8:
                column = 1
            else:
                column = day_value
            content = content + columnlist(page, column, Range)[i]
            if header == "vegetables":
                content = ""
            if content != "":
                content = addemojiscontent(content)
                response = "".join([response,str(header).title(),": \n",str(content).capitalize(),"\n\n"])
                #response = response + str(header).title() + ": \n" + str(content).capitalize() + "\n\n"
        except IndexError:
            print('NOK')
    # if "Oven roast barramundi" in response:
    #     response = response + u"\nHmm... sounds like a roundy run to me... \U0001F914 \n"
    # elif "Roast turkey" in response:
    #     response = "Dino changed dinner but heres what it's supposed to be:\n\n" + response
    # response = addemojisresponse(response)
    #print("dinnermenu DONE")
    return response

def addemojis(header):
    #print("addemojisheader")
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
    #print("addemojisheader DONE")
    return header

def addemojiscontent(content):
    #print("addemojiscontent")
    #content = content.replace("egg", u"egg \U0001F95A")
    content = content.replace("pancakes", u"pancakes \U0001f95e")
    content = content.replace("pizza", u"pizza \U0001f355")
    content = content.replace("sushi", u"sushi \U0001f363")
    content = content.replace("chicken", u"chicken \U0001F357")
    content = content.replace("honey", u"honey \U0001F36F")
    #print("addemojiscontent DONE")
    return content

# def addemojisresponse(response):
#     if "vegetarian option" in response:
#         response = response.replace("vegetarian option", u"vegetarian option \U0001F331")
#     else:
#         response = response.replace("vegetarian", u"vegetarian \U0001F331")
#     response = response.replace("main course", u"main course \U0001F37D").replace("hot option", u"hot option \U0001F37D")
#     response = response.replace("residential breakfast", u"residential breakfast \U0001f95e")
#     response = response.replace("soup", u"soup \U0001f372")
#     response = response.replace("the dessert station", u"the dessert station \U0001f370")
#     response = response.replace("additional vegetables", u"additional vegetables \U0001F966")

#     response = response.replace("pancakes", u"pancakes \U0001f95e")
#     response = response.replace("pizza", u"pizza \U0001f355")
#     response = response.replace("sushi", u"sushi \U0001f363")
#     response = response.replace("chicken", u"chicken \U0001F357")
#     response = response.replace("honey", u"honey \U0001F36F")
#     return response


def columnlist(page, column, Range): #gets the info from each column as a list
    #print("columlist")
    #global row
    #global column
    rowcontents = []
    for i in range(0,Range):
        row = i
        content = getinfo(page, row, column)
        rowcontents.append(content)
    #print("columlist DONE")
    return rowcontents

def addnote(con, value, day):
    #print("addnote")
    meal = value
    if day == "Today": #makes sure we are talking about the actual day e.g. not tommorrow or the coming wednesday
        note = read_custom_message(meal, con)
    else: #otherwise there is no note
        note = None 

    if note is not None:
        note = "Note:\n" + note.capitalize()

    #print("addnote DONE")
    return note


def getinfo(page, row, column):
    #print("getinfo")
    #global page
    #global row
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
            #plain_text  =  stuff.strip(""",.;:-¢"'�_!?I•,L4J£<~""") #removes all weird artifacts
            info.append(stuff)
        else:
            print("none!")
    #print(str(row) + str(column) + "row column")
    #print(info[column])
    #print("getinfo DONE")
    return info[column]


