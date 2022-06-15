'''
Gets the content of what the meal is based on given
meal, day name and day number parameters
'''

from datetime import *
from pytz import timezone

from menu_to_df import get_df

TIMEZONE = timezone('Australia/Sydney')
MENU_DIRECTORY = './menu_weeks'

meals_attributes = {
	'breakfast': {
		'headers': [u"Residential Breakfast \U0001f95e", 
					"Special"],
		'start': 0,
	},
	'lunch': {
		'headers': [u"Hot Option \U0001F37D", 
					u"Vegetarian Option \U0001F331"], 
					#u"Soup \U0001f372"],
		'start': 0,

	},
	'dinner': {
		'headers': [u"Main Course \U0001F37D", 
					u"Vegetarian \U0001F331", 
					u"Salad \U0001F957", 
					"Vegetables", 
					u"Additional Vegetables \U0001F966", 
					u"The Dessert Station \U0001f370"],
		'start': 2,
	},
}

class Meal:
	def __init__(self, mealtype):
		self.name = mealtype
		self.attributes = meals_attributes[mealtype]
		self.headers = self.attributes['headers']
		self.start = self.attributes['start']

	def getresponse(self, day_name, day_number, week):
		print(f'Day Number {day_number}')

		self.response = f"{self.name} {day_name}: \n".title()

		column_list = (get_df(self.name, week)[day_number + 1])

		# Below filters 'nan' from the list which is a float
		column_list = list(filter(lambda v: v == v, column_list[self.start:]))
		
		for idx, header in enumerate(self.headers):
			if header == 'Vegetables':
				continue
			content = column_list[idx]
			# Pandas duplicates across merged cells
			# so we make sure not to add duplicates
			content = addemojiscontent(content.strip())
			if content not in self.response:
				self.response += f"{header}:\n {content}\n"
		
		return self.response


def addemojiscontent(content):
	#content = content.replace("egg", u"egg \U0001F95A")
	content = content.replace("pancakes", u"pancakes \U0001f95e")
	content = content.replace("pizza", u"pizza \U0001f355")
	content = content.replace("sushi", u"sushi \U0001f363")
	content = content.replace("chicken", u"chicken \U0001F357")
	#content = content.replace("honey", u"honey \U0001F36F")
	return content


if __name__ == '__main__':
	# for i in range(1,8):
	week = 1
	print(Meal('breakfast').getresponse('Today', 2, week))
	print(Meal('lunch').getresponse('Tomorrow', 3, week))
	print(Meal('dinner').getresponse('Tomorrow', 3, week))