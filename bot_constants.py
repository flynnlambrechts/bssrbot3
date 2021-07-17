#Constants
import os
from pytz import timezone

TIMEZONE = timezone('Australia/Sydney')

ACCESS_TOKEN = os.environ['ACCESS_TOKEN'] #used for fb connection
VERIFY_TOKEN = os.environ['VERIFY_TOKEN'] #used to verify fb
DATABASE_URL = os.environ['DATABASE_URL']

Admin_ID = ["4409117335852974", #Flynn-DEV
            "3760608700732342" #Flynn-REAL
] #id of users with powerful permission

Staff_ID = ["3963292617085764", #Kendy
"4294576107270093", #Sam
"4610989705596963", #Kyra
"3890926854296476" #James
]

dino_quickreplies = [{'content_type': 'text', 'title': 'Breakfast', 'payload': 'Breakfast'},\
 {'content_type': 'text', 'title': 'Lunch', 'payload': 'Lunch'},\
 {'content_type': 'text', 'title': 'Dinner', 'payload': 'Dinner'},\
 {'content_type': 'text', 'title': 'Dino', 'payload': 'Dino'}]
 #{'content_type': 'text', 'title': 'All', 'payload': 'All'}]

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

#Basser used in get_bot_response
bassertimes = {"breakfast": "7:00-7:45am",\
"lunch" : "11:45-12:30pm",\
"dinner" : "4:30-5:15pm"}
dinotimes = "".join(["Basser Dino Times: \nBreakfast: ", bassertimes["breakfast"], "\nLunch: ", bassertimes["lunch"], "\nDinner: ", bassertimes["dinner"]])

notbassertimes = {"Baxter" : "Baxter Dino Times:\nBreakfast: 8:00-8:45am\nLunch: 12:45-1:30pm\nDinner: 5:45-6:30pm",\
"Goldstein" : "Goldstein Dino Times:\nBreakfast: 9:00-9:45am\nLunch: 1:45-2:30pm\nDinner: 6:45-7:30pm",\
"Fig" : "Fig Tree Dino Times:\nBreakfast: 9:00-9:45am\nLunch: 1:45-2:30pm\nDinner: 6:45-7:30pm",\
"Hall" : "Hall Dino Times:\nBreakfast: As Normal \nDinner: 7:45-8:30pm"}

#used in TheScrape3
week_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

#DEFINED IN THESCRAPE3 IN CLASS UPDATE THERE
# breakfastheaders = [u"Residential Breakfast \U0001f95e", "Special"]
# lunchheaders = [ u"Hot Option \U0001F37D", u"Vegetarian Option \U0001F331", u"Soup \U0001f372"]
# dinnerheaders = [u"Main Course \U0001F37D", u"Vegetarian \U0001F331", u"Salad \U0001F957", "Vegetables", u"Additional Vegetables \U0001F966", u"The Dessert Station \U0001f370"]



