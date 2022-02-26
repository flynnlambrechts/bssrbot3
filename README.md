# BssrBot 3.5.1
> Basser's Dino Menu, Shop and Calendar Assistant

## Requirements

Wit.ai - Language process (no longer used)
Heroku - Hosting code
NewRelic https://elements.heroku.com/addons/newrelic - Prevents code from idling
Database: postgresql - stores information input by users

## To Do
- Dino - done
- Shopen - done
- Add shop catalogue -done
- Calendar - done
- Wildcat of the week nominations
- Ressies
- BssrBot v4

## On Boarding of New Admin
1. Facebook for Developers
- Add admin to app roles as administrator for both BssrBot and BssrBot-Dev
2. Heroku
- Add as collaborator on both BssrBot and BssrBot-Dev
	- app -> overview -> collaborator activity -> manage access -> add collaborator
3. GitHub
- Add as collaborator on both bssrbot3 and bssrbot-dev
	- settings -> manage access -> add people
4. Hard code
- Add psid as seen from both bssrbot and bssrbot-dev to ADMIN_ID in ./bot_constants
5. Add to facebook pages for both forms of the bot.
6. Run through updating process and supply camelot.py file to extract dino meals. Also ensure set up with postgresql to connect and manage DB.


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
- So much more

## Work On
- clean up shopen

## BssrBot v4 Coming Features
### Coffee Night
- Wildcat of the week Nominations
	- working just need to find a way to send back
- Quote of the week submission
- Photo submissions (for slide show)
- Coffee Night Notificaitons? (Opt in and opt out)
### Usability
- Set week of term easier (admin)
- Set week of dino easier (admin)
- Register users college

Github# bssrbot-dev
