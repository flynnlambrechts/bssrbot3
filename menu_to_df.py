'''
Converts the pdf file into seperate html files
Then provides a function to extract a pandas
dataframe from this file.

Note this is not used during normal use
Only when updating the menu
'''

from bs4 import BeautifulSoup
# Importing BeautifulSoup class from the bs4 module

import os
import pandas as pd

MENU_DIRECTORY = "./menu_weeks"

def open_pdf():
#-----------------------Opening the HTML file--------------------------#
	HTMLFile = open(str("menu.html"), "r") #try putting in func.
	#print(str(HTMLFile))
	# Reading the file
	index = HTMLFile.read()
	  
	# Creating a BeautifulSoup object and specifying the parser
	soup = BeautifulSoup(index, 'lxml')

	# Using the prettify method to modify the code
	# print(soup.body.prettify())

	# print(soup.title) #prints the table title if it has one

	#make a folder for menus to drop into
	if not os.path.exists(MENU_DIRECTORY):
		os.makedirs(MENU_DIRECTORY)


	names = []
	for number, table in enumerate(soup.find_all("table")):
		name = "Unknown"
		if number%4 == 0:
			continue
		elif (number-1)%4 == 0:
			name = f"B_{int((number+3)/4)}"
		elif (number-2)%4 == 0:
			name = f"L_{int((number+2)/4)}"
		elif (number-3)%4 == 0:
			name = f"D_{int((number+1)/4)}"
		names.append(name)

		save_table(table, name)

	print(f"Html files created with names: {names} at location {MENU_DIRECTORY}")
	return

def save_table(data, name):
	with open(f"{MENU_DIRECTORY}/{name}.html", "w") as f:
		f.write(str(data))

def get_df(meal, week):
	''' Gets the dataframe given a meal and week'''
	meal_keys = {'breakfast': 'B', 'lunch': 'L', 'dinner': "D"}
	return pd.read_html(f"{MENU_DIRECTORY}/{meal_keys[meal]}_{week}.html")[0]


if __name__ == "__main__":
	open_pdf()
	
