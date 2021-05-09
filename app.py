  
#Python libraries that we need to import for our bot

import os, sys
from datetime import *
import random
import time
import calendar
import pytz
import psycopg2
import requests

from flask import Flask, request
from pymessenger.bot import Bot

from utils import wit_response
from TheScrape2 import checkForDino
from EasterEggs import checkForEasterEggs
from shopen import *
from connectdb import connectToDB
connectToDB()
from connectdb import con
global con

global week
week = 1 ### work out how to define the week

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)
flynn_id = "m_bTL21NIhMZzHHCSOYymKdklxKBtona4_wMjcO42dp0FzeQZu367t8TLnsdDkusnEFT5-LjUTcxLpNjXbfkgQ_Q"
TIMEZONE = pytz.timezone('Australia/Sydney')



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
       #log(output) #entire output good for finding sender ids what message contains etc
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                global recipient_id
                recipient_id = message['sender']['id']
                
                #if it has text
                if message['message'].get('text'):
                    message_text = message['message']['text']
                    print(message_text)
                    response_sent_text = get_bot_response(message_text)
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = "Nice pic!"
                    send_message(recipient_id, response_sent_nontext)

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

def get_bot_response(message_text):
    global con
    global message
    message = message_text.lower()
    global response
    response = ""
    global value, entity
    entity, value = wit_response(message) #prev message_text
    if entity == 'mealtype:mealtype':
        #response = "Ok i will tell you what {} is".format(str(value))
        response = response + checkForDino(message)
    elif checkIfGreeting(message):
        response = response + "Hello! Welcome to the Basser Bot! I'm here to help you with all your dino and calendar needs."
        response = response + (f" Here are some example questions:\n1. What's for dino? \n2. What's for lunch today? \n3. Is shopen?")
    elif message == "thx" or message == "thanks" or message == "thank you":
        response.append("You're welcome!")
    elif checkForShopen(message):
        response = response + checkForShopen(message)
    elif checkForEasterEggs(message):
        response = response + checkForEasterEggs(message)
    elif "my name" in message:
        response = response + getname(message)
    else:
        response = response + "Sorry, I don't understand"
        #con.close()
    return response

def getname(message):
    global recipient_id
    USER_ID = recipient_id
    global ACCESS_TOKEN
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
    


def checkIfGreeting(message):
    possibleGreetings = ["hello", "hi", "help", "hey"]
    message_elements = message.split()
    for word in message_elements:
        for el in possibleGreetings:
            if el == word:
                return True      
    return False

def checkForShopen(message):
    global con
    name = getname(message)
    response = ""
##only use once----------------------------------
    if "dookie:create table" in message:#        |
        response = response  + create_shopen()#  |
    elif "dookie:insert row" in message:#        |
        response = response + insert_shopen()#   |
##-----------------------------------------------
    if "i would like to open the shop" in message:
        response = response + open_shopen(name)
    elif "i would like to close the shop" in message:
        ##add feature where only person who opened can close
        response = response + close_shopen(name)
    elif "shopen" in message:
        response = response + get_shopen()
    return response


#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    global con
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    con.close()
    return "success"


if __name__ == "__main__":
    app.run()


