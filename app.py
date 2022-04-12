
# Python libraries that we need to import for our bot
import os
import sys  # for heroku env
import psycopg2  # database stuff
import json

from flask import Flask, request  # flask

from response import Response
from get_bot_response import get_bot_response, handle_postback
from models import Sender
from bot_constants import (VERIFY_TOKEN, Admin_ID)
from bot_functions import (PrintException, getCon)

app = Flask(__name__)

#Developer: Flynn
# Contributors: Ethan, Jas, Zoe

# We will receive messages that Facebook sends our bot at this endpoint


@app.route("/webhook", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
    try:
        if output:
            # print(request.json())
            log(output) #entire output good for finding sender ids what message contains etc
            for event in output['entry']:
                messaging = event['messaging']
                for message in messaging:
                    if message.get('message'):
                        recipient_id = str(message['sender']['id'])
                        #print(str(recipient_id) + " PSID"
                            
                        if message['message'].get('text'):
                            message_text = message['message']['text']
                            print(message_text)
                            get_bot_response(recipient_id, message_text)

                            con = getCon()
                            Sender(recipient_id).adduser(con)
                            con.close()
                            return "Text proccessed"
                        elif message['message'].get('attachments'):
                            attachment_url = message['message']['attachments'][0]['payload']['url']
                            print(attachment_url)
                            for attachment in message['message']['attachments']:
                                if attachment['type'] == 'image' and 'sticker_id' not in attachment['payload']:
                                    attachment_url = attachment['payload']['url']
                                    get_bot_response(recipient_id, attachment=attachment_url)
                                else:
                                    get_bot_response(recipient_id, attachment='invalid_type')
                        else:
                            print("No message?")
                            log(output)
                    elif message.get('postback'):
                        recipient_id = str(message['sender']['id'])
                        postback = message['postback']['payload']
                        handle_postback(recipient_id, message['postback'])
        else:
            print('PING!')
    except:
        PrintException()
        #alert_admin
    return "Message Processed"



def log(message):
    print(message)
    sys.stdout.flush()

def alert_admin():
    for ID in Admin_ID:
            response = Response(ID)
            response.text = "Oh no something went wrong :("
            response.send()

def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


if __name__ == "__main__":
    app.run()
