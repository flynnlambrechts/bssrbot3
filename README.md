# BssrBot 3.2.1
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

## Work On
- day next week and week = 4 - SOLVED
- why does Monday lunch work but not lunch Monday - SOLVED
- connecting to DB - SOLVED
- calendar - IN PROGRESS


Github# bssrbot-dev
