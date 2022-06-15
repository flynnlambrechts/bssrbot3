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
- Calendar - Done
- Wildcat of the week nominations
- Add images
- Add quotes
- Wildcat nominations
- Ressies


## To Update menu
1. Name menu "menu.pdf" and place and in menu folder (remove old menu items)
1. Open menu pdf in Adobe Acrobat and export file
to html named 'menu.html'
2. Run menu_to_df.py to generate individual menu htmls
3. In the get_dino find what week of the year corresponds to current menu week and update subtract value


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

Github# bssrbot3