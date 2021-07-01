  
#Python libraries that we need to import for our bot

import os, sys                          #for heroku env
from datetime import *                  #for time proccessing
#import random                           #for random generation
import time                             #for time
#import calendar                        #not neccessary
import pytz                             #timezone
import psycopg2                         #database stuff
import requests                         #for sending get request
import json

from flask import Flask, request        #flask
#from pymessenger.bot import Bot        #library for sending messages no longer used

from utils import wit_response          #for nlp
from TheScrape2 import checkForDino     #for scraping htmls
from TheScrape2 import dinotimes        #pulls the dino times from the scrape
from TheScrape2 import checkForButton   #Checks whether should add feedback button
from EasterEggs import checkForEasterEggs #self explanatory
from shopen import *                    #for all shopen related
from killswitch import add_custom_message
from calendar1 import get_events
from jokes import getjoke               #for jokes
from shop_catalogue import shop_catalogue 
from otherdinotimes import notBasser

from users import *                     #for viewing users
from getmenuweek import checkForDay

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN'] #used for fb connection
VERIFY_TOKEN = os.environ['VERIFY_TOKEN'] #used to verify fb
Admin_ID = ["4409117335852974", #Flynn-DEV
            "3760608700732342" #Flynn-REAL
            ] #id of users with powerful permission
#bot = Bot(ACCESS_TOKEN) #not sure
TIMEZONE = pytz.timezone('Australia/Sydney') #sets timezone

#Developer: Flynn
#Contributors: Ethan, Jas, Zoe


def getCon(): #gets the connection  to the database when required
    if "HEROKU" in os.environ:
        DATABASE_URL =  os.environ['DATABASE_URL']
        con = psycopg2.connect(DATABASE_URL, sslmode='require')
    else:
        con = psycopg2.connect(database="bssrbot1", user="flynnlambrechts", password="", host="127.0.0.1", port="5432")
        print("Local Database opened successfully")
    return con


#----------------------------------------------------------------------------------------------


#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
#try:
    #log(output) #entire output good for finding sender ids what message contains etc
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
          if message.get('message'):
            #Facebook Messenger ID for user so we know where to send response back to
            #global recipient_id
            recipient_id = message['sender']['id']
            #global buttons
            #if it has text
            if message['message'].get('text'):
                message_text = message['message']['text']
                print(message_text)
                response_sent_text, buttons = get_bot_response(message_text, recipient_id)
                send_message(recipient_id, response_sent_text, buttons)
            #if user sends us a GIF, photo,video, or any other non-text item
            elif message['message'].get('attachments'):
                #response = "Hello"
                #send_other(recipient_id, response)
                buttons = []
                response_sent_nontext = "Nice pic!"
                send_message(recipient_id, response_sent_nontext, buttons)
#except TypeError: #if anti-idling add on pings bot we wont get an error
        #print('PING!')
#except:
        #print("an error occured...") 
    return "Message Processed"


def log(message):
    print(message)
    sys.stdout.flush()
    
def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a message to send to the user
def get_bot_response(message_text, recipient_id):
#--------------------------------------------------------------------------------------------------------------------------------------------------------   
    #global Admin_ID
    #global recipient_id
    #global message
    message = message_text.lower()
    #global response
    response = ""
    #global value, entity
    entity, value = wit_response(message) #prev message_text
    #global buttons
    buttons = []
#--------------------------------------------------------------------------------------------------------------------------------------------------------   
    if notBasser(message):
        response = notBasser(message)
    elif entity and "dookie:" not in message: #if user is asking for a meal (uses wit.ai)
        con = getCon()
        response = response + checkForDino(message, con, value)
        buttons = checkForButton(message)
        con.close()
    elif checkIfGreeting(message):
        response = response + "Hello! Welcome to the BssrBot! I'm here to help you with all your dino and calendar needs."
        response = response + (f" Here are some example questions:\n1. What's for dino? \n2. What's for lunch today? \n3. Is shopen? \n4. What's the shop catalogue? \n5. What's on tonight? \n6. Events on this week?")
        buttons = [{
                "type": "web_url",
                "url": "https://www.facebook.com/BssrBot-107323461505853/",
                "title": "BssrBot Page"
                }]
    elif "thx" in message or "thanks" in message or "thank you" in message or "thankyou" in message:
        response = response + "You're welcome!" + u"\U0001F60B" #tongue out emoji
    elif checkForShopen(message, recipient_id):
        response = response + checkForShopen(message, recipient_id)
    elif checkForCalendar(message):
        response = response + checkForCalendar(message)
    elif checkForEasterEggs(message):
        response = response + checkForEasterEggs(message)
    elif checkForDay(message) or "tomorrow" in message or "today" in message:
        response = response + "blank for now"
        buttons = [{
                "type": "web_url",
                "url": "https://user.resi.inloop.com.au/home",
                "title": "Latemeal"
                }]
    elif "time" in message:
        #global dinotimes
        response = response + dinotimes
    elif "latemeal" in message or "late" in message or "inloop" in message:
        response = "Order a late meal here:"
        buttons = [{
                "type": "web_url",
                "url": "https://user.resi.inloop.com.au/home",
                "title": "Latemeal"
                }]
    elif "my name" in message:
        response = response + getname(recipient_id)
    elif "gif" in message:
        response = "gif"
    elif "joke" in message:
        response = response + getjoke()
    elif "dookie:" in message and str(recipient_id) in Admin_ID: #for adding custom messages
        con = getCon()
        add_custom_message(message, con)
        response = response + "Adding custom message..."
        con.close()
    elif "show me users" in message:
        con = getCon()
        if str(recipient_id) in Admin_ID: 
            response = response + "Users: \n" + view_users(con)
        else:
            response = response + "You shall not, PASS: \n" + str(recipient_id)
        con.close()
    else:
        response = response + "Sorry, I don't understand: \n" + message
#--------------------------------------------------------------------------------------------------------------------------------------------------------
    return response, buttons

def getname(recipient_id): #gets user full name in format "F_name L_name"
    #global ACCESS_TOKEN
    URL = "https://graph.facebook.com/v2.6/"+ recipient_id + "?fields=first_name,last_name&access_token=" + ACCESS_TOKEN
    name = ""
    # sending get request and saving the response as response object
    r = requests.get(url = URL)
    # extracting data in json format
    data = r.json()
    first_name = data['first_name']
    last_name = data['last_name']
    name = str(first_name) + " " + str(last_name)
    #print("NAME: " + "'" + name + "'")
    return name

def getdetails(recipient_id): #gets user PSID and name details
    #global recipient_id
    #global ACCESS_TOKEN
    URL = "https://graph.facebook.com/v2.6/"+ recipient_id + "?fields=first_name,last_name&access_token=" + ACCESS_TOKEN
    r = requests.get(url = URL)
    data = r.json()
    first_name = data['first_name']
    last_name = data['last_name']
    full_name = str(first_name) + " " + str(last_name)
    PSID = int(recipient_id)
    return full_name, first_name, last_name, PSID

def adduser(con, recipient_id): #adds user to DB
    full_name, first_name, last_name, PSID = getdetails(recipient_id)
    insert_user(full_name, first_name, last_name, PSID, con)
    

def checkIfGreeting(message): #checks if the user sends a greeting
    possibleGreetings = ["hello", "hi", "help", "hey"]
    message_elements = message.split()
    for word in message_elements:
        for el in possibleGreetings:
            if el == word:
                return True      
    return False

def checkForShopen(message, recipient_id):
    con = getCon()
    name = getname(recipient_id)
    response = ""
    global shop_catalogue
    if shop_catalogue == None:
        #global shop_catalogue
        shop_catalogue = "No catalogue." + u"\U0001F4A9" #poop emoji
    
##----only use once---------or do in terminal-----
#    if "dookie:create table" in message:#        |
#        response = response  + create_shopen()#  |
#    elif "dookie:insert row" in message:#        |
#        response = response + insert_shopen()#   |
##------------------------------------------------
    if "i would like to open the shop" in message:
        response = response + open_shopen(name, con)
    elif "i would like to close the shop" in message:
        ##add feature where only person who opened can close
        response = response + close_shopen(name, con)
    elif "shopen" in message or ("shop" in message and ("catalogue" not in message and "sell" not in message)):
        response = response + get_shopen(con)
        response = response + "\n" + "\n" + shop_catalogue
    elif "catalogue" in message or ("shop" in message and "sell" in message):
            response = response + str(shop_catalogue)
    con.close()
    return response

def checkForCalendar(message):
    response = ""
    if "events" in message \
    or "event" in message \
    or "whats on" in message \
    or "what’s on" in message \
    or "what's on" in message \
    or "what is on" in message:
        con = getCon()
        response = response + get_events(message, con)
        con.close()
    return response


# def checkForKill(message):
#     if "dino wrong" in message and str(recipient_id) in Admin_ID:
#         con = getCon()
#         killswitch(message, con)
#         con.close()


#formerly uses PyMessenger to send response to user
#now routes to send message with or without buttons
def send_message(recipient_id, response, buttons): #decides what type of respones to send
    if recipient_id == "5443690809005509": #CHECKS IF HUGO IS MESSAGING
        response = response + "\n\nSHUTUP HUGO"
    #sends user the text message provided via input response parameter
    #print("test")
    if buttons != []:
        #text = str(response)
        #bot.send_button_message(recipient_id, text, url_button)
        send_buttons(recipient_id, response, buttons)
    elif response == "gif":
        message = "nice"
        send_gif_message(recipient_id, message)
    else:
        #bot.send_text_message(recipient_id, response)
        send_nonbuttons(recipient_id, response)
    con = getCon()
    adduser(con, recipient_id)
    con.close()
    return "success"


#sends response with quick replies and button
def send_buttons(recipient_id, response, buttons): #change to send button message
    start = datetime.datetime.now(TIMEZONE).timestamp()
    params = {
           "access_token": os.environ["ACCESS_TOKEN"]
    }

    headers = {
            "Content-Type": "application/json"
    }
    #message_text = str(response)
    # buttons = [{
    #             "type": "web_url",
    #             "url": "https://bit.ly/3hVT0DX",
    #             "title": "Leave Feedback"
    #             },
    #             {
    #             "type": "web_url",
    #             "url": "https://user.resi.inloop.com.au/home",
    #             "title": "Latemeal"
    #             }
    #             ]
    #print(type(buttons))
    data = json.dumps({
                "recipient": {
                    "id": recipient_id
                },
                "message": {
                    "attachment":{
                        "type":"template",
                        "payload":{
                            "template_type":"button",
                            "text":str(response),
                            "buttons": buttons
                        }
                    },
                    "quick_replies":[{
                            "content_type":"text",
                            "title":"Breakfast",
                            "payload":"Breakfast"
                            },
                            {
                            "content_type":"text",
                            "title":"Lunch",
                            "payload":"Lunch"
                            },
                            {
                            "content_type":"text",
                            "title":"Dinner",
                            "payload":"Dinner"
                            },
                            {
                            "content_type":"text",
                            "title":"Dino",
                            "payload":"Dino"
                            }]
                }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    end = datetime.datetime.now(TIMEZONE).timestamp()
    print(str(end - start) + " send buttons")
    return "other sent"

def send_nonbuttons(recipient_id, response):
    message_text = str(response)
    params = {
           "access_token": os.environ["ACCESS_TOKEN"]
    }

    headers = {
            "Content-Type": "application/json"
    }

    data = json.dumps({
               "recipient": {
                      "id": recipient_id
               },
               "message": {
                    "text": message_text,
                    "quick_replies":[{
                            "content_type":"text",
                            "title":"Breakfast",
                            "payload":"Breakfast"
                            },
                            {
                            "content_type":"text",
                            "title":"Lunch",
                            "payload":"Lunch"
                            },
                            {
                            "content_type":"text",
                            "title":"Dinner",
                            "payload":"Dinner"
                            },
                            {
                            "content_type":"text",
                            "title":"Dino",
                            "payload":"Dino"
                            }]
               }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


def send_gif_message(recipient_id, message):
    gif_url = search_gif(message)

    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": gif_url
                }
            }}
    })

    params = {
        "access_token": os.environ["ACCESS_TOKEN"]
    }

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)


if __name__ == "__main__":
    app.run()


def search_gif(text):
    #get a GIF that is similar to text sent
    payload = {'s': text, 'api_key': 'ey1oVnN1NGrtEDHFGBJjRj5AgegLFVeT', 'weirdness': 1}
    r = requests.get('http://api.giphy.com/v1/gifs/translate', params=payload)
    r = r.json()
    # sprint(r)
    try:
        url = r['data']['images']['original']['url']
    except:
        print('failed to get gif')

    return url



