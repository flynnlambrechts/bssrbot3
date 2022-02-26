#TheScrape2 IS NOW A RELIC OF THE PAST (NO LONGER IN USE)
#She is very slow but is accurate i think
#Kept around as a last resort if TheScrape3 has mistakes
from datetime import *
import time
from pytz import timezone
TIMEZONE = timezone('Australia/Sydney')

from bs4 import BeautifulSoup # Importing BeautifulSoup class from the bs4 module

from killswitch import read_custom_message

#define the dino times here used throughout
from bot_constants import (bassertimes, dinotimes)

def checkForDino(message, con, value):
    week = getmenuweek()

    response = ""
    
    day, current_day, column, week = getDay(message, week) #checks for days and creates current_day
    #current_day: day of week 0-6 inclusive
    #day_value: day of week 1-7 inclusive
    #day: name of the day e.g. monday, wednesday, tomorrow, today
    #week: week of cycle (1-4)

    time = datetime.now(TIMEZONE).time().hour
    
    if value == "dino": #handling if meal is non-specified
        if "time" in message:
            response = response + dinotimes
        elif day == "Tomorrow":
            response = response + (f"Dino Breakfast Tomorrow: \n")
            day_value = current_day + 1
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
            response = response + dinnermenu(day_value, column, week)
        else: 
            response = response + (f"Breakfast Tomorrow: \n")
            day_value = int(datetime.now(TIMEZONE).weekday()) + 2 #this is 2 since early +1 was done cause "tomorrow" was in message
            response = response + breakfastmenu(day_value, column, week)
    elif value == "breakfast":
        if "time" in message:
            response = response + "Basser breakfast is at " +  bassertimes["breakfast"]
        elif time > 14 and day == "Today": #after 2pm will give the breakfast for the next day
            day = "Tomorrow"
            response = response + (f"Breakfast {day}: \n")
            day_value = current_day + 2
            current_day += 1
            time = 0
            if current_day==7:
                if week==4:
                    week = 1
                    print(str(week) + " week")
                    column = 1
                else:
                    week = week + 1
                    print(str(week) + "week")
                    column = 1
            response = response + breakfastmenu(day_value, column, week)
        else:
            response = response + (f"Breakfast {day}: \n")
            day_value = current_day + 1
            response = response + breakfastmenu(day_value, column, week)
        
    elif value == "lunch":
        if "time" in message:
            response = response + "Basser lunch is at " + bassertimes["lunch"]
        elif time > 17 and day == "Today": #after 5pm will give the lunch for the next day
            day = "Tomorrow"
            response = response + (f"Lunch {day}: \n")
            day_value = current_day + 2
            current_day += 1
            time = 0
            if current_day==7:
                if week==4:
                    week = 1
                    print(str(week) + " week")
                    column = 1
                else:
                    week = week + 1
                    print(str(week) + "week")
                    column = 1
            response = response + lunchmenu(day_value, column, week)
        else:
            response = response + (f"Lunch {day}: \n")
            day_value = current_day + 1
            response = response + lunchmenu(day_value, column, week)

    elif value == "dinner":
        if "time" in message:
            response = response + "Basser dinner is at " + bassertimes["dinner"]
        elif time > 20 and day == "Today": #after 8pm will give the value for the next day
            day = "Tomorrow"
            response = response + (f"Dinner {day}: \n")
            day_value = current_day + 2
            current_day += 1
            time = 0
            if current_day==7:
                if week==4:
                    week = 1
                    print(str(week) + " week")
                    column = 1
                else:
                    week = week + 1
                    print(str(week) + "week")
                    column = 1
            response = response + dinnermenu(day_value, column, week)
        else:
            response = response + (f"Dinner {day}: \n")
            day_value = current_day + 1
            response = response + dinnermenu(day_value, column, week)

    if "time" not in message:
        note = addnote(con, value, day)
    else:
        note = None
    if note is not None:
        response = response + str(note)

    return response

def getDay(message, week): #here is where we get the day and current_day and sometimes week
    column = ""

    current_day = datetime.now(TIMEZONE).weekday()
    day = "Today"
    
    #See if user is asking about tomorrow
    if "tomorrow" in message or "tmrw" in message or "tomoz" in message or "tmoz" in message:
        day = "Tomorrow"
        current_day+=1
        time = 0

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
    elif check_for_day(message):
        print("day found")
        week_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        if current_day > int(check_for_day(message)):
            print(str(week) + " week")
            if str(week)==str("4"):
                week = 1
                print(str(week) + " week")
            else:
                week = week + 1
                print(str(week) + " week")
            current_day = int(check_for_day(message))
            day = str(week_days[int(check_for_day(message))])
        else:
            current_day = int(check_for_day(message))
            day = str(week_days[int(check_for_day(message))])
    #otherwise must be today: and day and current_day are not updated from todays value
    return day, current_day, column, week

    

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
#     elif check_for_day(message):


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
    content = content.replace("pancakes", u"pancakes \U0001f95e")
    content = content.replace("pizza", u"pizza \U0001f355")
    content = content.replace("sushi", u"sushi \U0001f363")
    content = content.replace("chicken", u"chicken \U0001F357")
    content = content.replace("honey", u"honey \U0001F36F")
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
    rowcontents = []
    for i in range(0,Range):
        row = i
        content = getinfo(page, row, column)
        rowcontents.append(content)
    return rowcontents

def addnote(con, value, day):
    meal = value
    if day == "Today": #makes sure we are talking about the actual day e.g. not tommorrow or the coming wednesday
        try: 
            note = "".join(["Note:\n",read_custom_message(meal, con).capitalize()])
        except AttributeError:
            note = None
    else: #otherwise there is no note
        note = None 

    return note


def getinfo(page, row, column):
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


def getmenuweek():
    TIMEZONE = timezone('Australia/Sydney')
    x = datetime.datetime.now(TIMEZONE)
    week = (int(x.strftime("%W"))+1) #plus one changes the cycle to match the dino cycle
    menuweek = (week)%4+1 #this cheeky +1 changes range from (0-3 to 1-4)
    print(menuweek)
    return menuweek

def check_for_day(message): #check of day of week specified
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



