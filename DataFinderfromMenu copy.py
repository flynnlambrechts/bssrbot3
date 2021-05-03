# Importing BeautifulSoup class from the bs4 module
from bs4 import BeautifulSoup
import requests
import re

#from app import value

week = int(1) ### work out how to define the week

global column
column = 4
global day_value
day_value = 4
global row
row = 2
page = str(1)


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

def getinfo(column):
    info = []
    global menu_table_data
    global row
    for td in menu_table_data[row].find_all("td"):
        if td is not None:
            plain_text = str(td).replace(r" \n",", ")
            info.append(plain_text.replace("<td>","").replace("</td>","").replace("amp;",""))
        else:
             print("none!")
    return info[column]
    #print(info[column])
'''
def columnlist(i):
    global row
    global column
    rowheaders = []
    #for i in range(0,2):
    print(i)
    row = i
    header = getinfo(column)
    rowheaders.append(header)
    print(rowheaders)
    return rowheaders[i]


def breakfastmenu():
    global column
    global row
    response = ""
    for i in range(0,1):
        column = 0
        header = str(columnlist(i)).title() +": "
        response = response + header
        column = day_value
        contents = str(columnlist(i))
        response = response + contents
    return response
'''

def breakfastmenu():
    global column
    global Range
    Range = int("2")
    response = ""
    for i in range(0,Range):   
        header = ""
        column = 0
        header = header + columnlist()[i]
        content = ""
        column = day_value
        content = content + columnlist()[i]
        response = response + str(header).title() + ": " + str(content) + "\n"
    return response

def columnlist():
    global row
    global column
    rowcontents = []
    for i in range(0,Range):
        print(i)
        row = i
        content = getinfo(column)
        rowcontents.append(content)
    return rowcontents

print(breakfastmenu())


#global response
#response = []
'''
def runLoop(response):
    global row
    for i in range(0,2):
        #response = ["test"]
        column = 0
        print(i)
    
        row = i
        print(getinfo(column))
        info = getinfo(column)
        response.append(info)
        print(response)
    return response 


response = []
response = runLoop(response)
print(response[0])
'''
#print(getinfo(column))

