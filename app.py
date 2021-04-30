  
#Python libraries that we need to import for our bot

import os, sys
import random

from flask import Flask, request
from pymessenger.bot import Bot

from utils import wit_response

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)
flynn_id = "m_bTL21NIhMZzHHCSOYymKdklxKBtona4_wMjcO42dp0FzeQZu367t8TLnsdDkusnEFT5-LjUTcxLpNjXbfkgQ_Q"

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
       log(output)
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                
                #if it has text
                if message['message'].get('text'):
                    message_text = message['message']['text']
                    response_sent_text = get_bot_response(message_text)
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
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
    message = message_text.lower()
    global response
    response = ""
    entity, value = wit_response(message) #prev message_text
    if entity == 'mealtype:mealtype':
        response = "Ok i will tell you what {} is".format(str(value))
        response = response + checkForDino(message)
    elif checkIfGreeting(message):
        response = response + "Hello! Welcome to the Basser Bot! I'm here to help you with all your dino and calendar needs."
        response = response + (f" Here are some example questions:\n1. What's for dino? \n2. What's for lunch today? \n3. What's the calendar for this week? \n4. What's happening on Thursday? \n5. Is shopen?")
    elif message == "thx" or message == "thanks" or message == "thank you":
        response.append("You're welcome!")
    elif message == "random":
        sample_responses = ["ben is a cockboy","molly farted","crispy is a simp","mitchy is thick","hugo is sick"]
        # return selected item to the user
        response = response + random.choice(sample_responses)
    elif message == "updog":
        response = response + "What is updog?"
    else:
        response = response + "Sorry, I don't understand"
    return response


def checkIfGreeting(message):
    possibleGreetings = ["hello", "hi", "help", "hey"]
    message_elements = message.split()
    for word in message_elements:
        for el in possibleGreetings:
            if el == word:
                return True      
    return False

def checkForDino(message):
    response = ""
    current_day = datetime.now(TIMEZONE).weekday()
    time = datetime.now(TIMEZONE).time().hour
    day = "today"
    
    #See if user is asking about tomorrow
    if "tomorrow" in message:
        day = "tomorrow"
        current_day+=1
        time = 0
        reponse = response + "tomorrow"
        if current_day==7:
            response + "Sorry, do not have the menu for next week yet!"
            return response
        
    #todayMenu = getDayMenu(current_day)
    
    #handling if meal is non-specified
    if value == "dino" or "cooking good looking" in message:
        if time < 10:
            response + (f"For breakfast {day} is:")
            #response + (todayMenu.breakfast)
        if time < 14:
            response + (f"For lunch {day} is:")
            #response + (str(todayMenu.lunch))
        if time < 19:
            response + (f"For dinner {day} is:")
            #response + (str(todayMenu.dinner))
        if not response: 
            response + "No more meals today :)"
    elif value == breakfast:
        response + (f"For breakfast {day} is:")
        #response + (todayMenu.breakfast)
    elif value == lunch:
        response + (f"For lunch {day} is:")
        #response + (str(todayMenu.lunch))
    elif value == dinner:
        response + (f"For dinner {day} is:")
        #response + (str(todayMenu.dinner))
    return response
    


#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()


