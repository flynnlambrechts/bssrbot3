# Constants
import os
from pytz import timezone

TIMEZONE = timezone('Australia/Sydney')

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']  # used for fb connection
ACCESS_TOKEN_BACKUP = os.environ['ACCESS_TOKEN_BACKUP']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']  # used to verify fb
DATABASE_URL = os.environ['DATABASE_URL']
HOLIDAY_MODE = False
MENU_DIRECTORY = './menu_weeks'

Admin_ID = ["4409117335852974",  # Flynn-DEV
            "3760608700732342"  # Flynn-REAL
            ]  # id of users with powerful permission

Staff_ID = ["3963292617085764",  # Kendy
            "4294576107270093",  # Sam
            "4610989705596963",  # Kyra
            "3890926854296476",  # James
            "4522684851127792"  # mum
            ]

dino_quickreplies = [{'content_type': 'text', 'title': 'Breakfast', 'payload': 'Breakfast'},
                     {'content_type': 'text', 'title': 'Lunch', 'payload': 'Lunch'},
                     {'content_type': 'text', 'title': 'Dinner', 'payload': 'Dinner'},
                     {'content_type': 'text', 'title': 'Dino', 'payload': 'Dino'}]
# {'content_type': 'text', 'title': 'All', 'payload': 'All'}]

greeting_message = f"Hello! Welcome to BssrBot! I'm here to help you with all your dino and calendar needs.\
Here are some example questions:\
\n1. What's for dino? \
\n2. What's for lunch today? \
\n3. Is shopen? \
\n4. What's the shop catalogue? \
\n5. What's on tonight? \
\n6. Events on this week?"

shop_catalogue = u"Shop Currently Sells: \n\
Pods $3\n\
Pringles $4\n\
Tee Vee Snack $3\n\
Tiny Teddies $5 \U0001f43b\n\
Coke $1 \U0001f964\n\
Up n Go $ 1\n\
Drumstick $ 1\U0001f366\n\
Maggi Noodles $1\n\
Tonic Water $1\n\
10 Pack Twinings Tea $1\n\
Oreo $1.5\n\
Tim Tams $2\n\
Maxi Bon $2\n\
Red Bull $2\n\
Pads $2\n\
Meegs $2.5\n\
Shapes $2.5\n\
Cadbury Blocks $2.5\n\
Red Rock Deli Chips $3"

# #Basser used in get_bot_response
bassertimes = {"breakfast": "7:30-10:00am",
               "lunch": "12:00-1:00pm",
               "dinner": "5:00-6:15pm",
               "seconds": "6:30-6:45pm, 7:45-8:00pm"}
dinotimes = "".join(["Dino Times: \nBreakfast: ", bassertimes["breakfast"],
                     "\nLunch: ", bassertimes["lunch"],
                     "\nDinner: ", bassertimes["dinner"],
                     "\n\nSeconds: ", bassertimes["seconds"]])

# no longer used this was a COVID thing
notbassertimes = {"Baxter": "Baxter Dino Times:\nBreakfast: 8:45-10:00am\nLunch: 1:15-2:15pm\nDinner: 6:15-7:15pm",
                  "Goldstein": "Goldstein Dino Times:\nBreakfast: 7:30-8:30am\nLunch: 12:00-1:00pm\nDinner: 5:00-6:00pm",
                  "Fig": "Fig Tree Dino Times:\nBreakfast: 7:30-8:30am\nLunch: 12:00-1:00pm\nDinner: 5:00-6:00pm",
                  "Hall": "Hall Dino Times:\nBreakfast: As Normal \nDinner: 7:30-8:15pm"}


#used in TheScrape3
week_days = ["Monday", "Tuesday", "Wednesday",
             "Thursday", "Friday", "Saturday", "Sunday"]

# DEFINED IN THESCRAPE3 IN CLASS UPDATE THERE
# breakfastheaders = [u"Residential Breakfast \U0001f95e", "Special"]
# lunchheaders = [ u"Hot Option \U0001F37D", u"Vegetarian Option \U0001F331", u"Soup \U0001f372"]
# dinnerheaders = [u"Main Course \U0001F37D", u"Vegetarian \U0001F331", u"Salad \U0001F957", "Vegetables", u"Additional Vegetables \U0001F966", u"The Dessert Station \U0001f370"]
