# BssrBot 3.2.2
> Basser's Dino Menu, Shop and Calendar Assistant

## Requirements

Wit.ai - Language process
Heroku - Hosting code
NewRelic https://elements.heroku.com/addons/newrelic - Prevents code from idling
Database: postgresql - stores information input by users

## To Do
- Dino - done
- Shopen - done
- Add shop catalogue -done
- Calendar - working on it
- Wildcat of the week nominations
- Ressies


## To Update menu
1. Name menu "menu.pdf" and place and in menu folder (remove old menu items)
2. Run camelot.py to generate menu htmls
3. In the thescrape2 find what week of the year corresponds to current menu week and update subtract value
4. (Optional) Reduce multiples of 4 in thescrape2 to only possible values

## To Update calendar
1. \copy data into db using heroku:
	\copy calendar FROM <path_to_calednar.csv> WITH (FORMAT CSV);
2. Go to calendar1 and zero week in getaway function
3. Push changes
### Formatting Calendar
- Make sure have a zero row at top with days in
- change nulls to blanks and then update line in calendar1

## Capabilities
- Return meal from Dino, breakfast, lunch and dinner
 	- including tomorrow and days of week
- Crack a joke
- Greetings
- Process pleasantries
- Get user's name
- Shopen
- Easter Eggs
- Shop catalogue
- Dinotimes
- Dino Feedback link
- Calendar
	- Week by week
	- Days
	- Week numbers
	- next week

## Work On
- calendar - IN PROGRESS
	add day by day
	add next week
	maybe add week number
- putting menu in db
- getting dessert

Github# bssrbot-dev
