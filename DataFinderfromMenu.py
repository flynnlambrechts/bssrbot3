# Importing BeautifulSoup class from the bs4 module
from bs4 import BeautifulSoup
import requests
import re

#from app import value

week = int(1) ### work out how to define the week

column = 1
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

#def getinfo():
info = []
for td in menu_table_data[row].find_all("td"):
    if td is not None:
        info.append(str(td).replace('<td>', '').replace('</td>', '').replace('\n', ''))
    else:
        print("none!")

print(info[column])
