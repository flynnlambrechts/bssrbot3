'''
Gets the content of what the meal is based on given
meal, day name and day number parameters
'''

from datetime import *
from pytz import timezone
from string import printable


from menu_to_df import get_df

TIMEZONE = timezone('Australia/Sydney')
MENU_DIRECTORY = './menu_weeks'

meals_attributes = {
	'breakfast': {
		'headers': [u"Residential Breakfast \U0001f95e", 
					"Special"],
		'start': 0,
		'end': 3,
	},
	'lunch': {
		'headers': [u"Hot Option \U0001F37D", 
					u"Vegetarian Option \U0001F331"], 
					#u"Soup \U0001f372"],
		'start': 0,
		'end': 3,

	},
	'dinner': {
		'headers': [u"Main Course \U0001F37D", 
					u"Vegetarian \U0001F331", 
					u"Salad \U0001F957", 
					"Vegetables", 
					u"Additional Vegetables \U0001F966", 
					u"The Dessert Station \U0001f370"],
		'start': 2,
		'end': None,

	},
}

class Meal:
	def __init__(self, mealtype):
		self.name = mealtype
		self.attributes = meals_attributes[mealtype]
		self.end = self.attributes['end']
		self.start = self.attributes['start']

	def getresponse(self, day_name, day_number, week):
		print(f'Day Number {day_number}')

		self.response = f"{self.name} {day_name}: \n".title()

		data_frame = get_df(self.name, week)

		# with open('dataframe.html', 'w') as f:
		# 	f.write(data_frame.to_html())
			
		headers = data_frame[0][self.start:self.end]
		content = data_frame[day_number+1][self.start:self.end]

		content_dict = dict(zip(headers,content))

		temp_content = ""
		temp_header = ""
		for header in content_dict:
			content = content_dict[header]

			if temp_header != header and header == header:
				if temp_content != "" and temp_header != 'vegetables':
					temp_header = addemojiscontent(temp_header.lower())
					temp_content = addemojiscontent(clean_content(temp_content.lower()))
					self.response += f"{temp_header.title()}:\n{temp_content.capitalize()}\n"
				temp_header = header
				temp_content = ""

			if header == header:
				temp_header = header
			if content == content and content not in temp_content:
				temp_content += (content + '\n')
			# print(header, temp_header)
			# print(content, temp_content)


		
		return self.response

def clean_content(content):
	return ''.join(filter(lambda x: x in printable, content))


emojis = {
	"pancakes": u"\U0001f95e",
	"sushi": u"\U0001f363",
	"chicken": u"\U0001F357",
	"salad": u"\U0001F957",
	"main course": u'\U0001F37D',
	'hot option': u'\U0001F37D',
	'vegetarian': u'\U0001F331', 
	'residential breakfast': u'\U0001f95e',
	"vegetarian": u"\U0001F331",
	"additional vegetables": u"\U0001F966",
	"the dessert station": u"\U0001f370",

	# "honey": u"\U0001F36F",
	# "egg": u"\U0001F95A",
}

def addemojiscontent(content):
	for emoji in emojis:
		content = content.replace(emoji, emoji + f' {emojis[emoji]}')
	return content


if __name__ == '__main__':
	# for i in range(1,8):
	week = 2
	print(Meal('breakfast').getresponse('Today', 3, week))
	print(Meal('lunch').getresponse('Tomorrow', 3, week))
	print(Meal('dinner').getresponse('Today', 0, week))
	print(Meal('dinner').getresponse('Tomorrow', 4, week))