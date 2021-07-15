#get_bot_response
import os
import psycopg2

from response import (Response, UrlButton, QuickReply, Gif, Image)

from bot_constants import *
from bot_functions import (PrintException, getCon)

#from TheScrape2 import checkForDino as getDino   #for scraping htmls
from TheScrape3 import getDino
from shopen import *                    #for all shopen related
from killswitch import add_custom_message
from calendar1 import get_events
from jokes import getjoke               #for jokes


from users import *                     #for viewing users
from TheScrape3 import checkForDay
#from utils import wit_response

from models import Sender

from rivescript import RiveScript
bot = RiveScript()
bot.load_directory("./brain")
bot.sort_replies()


def get_bot_response(recipient_id, message_text="", attachment = ""):
	message = message_text.lower()
	response  = Response(recipient_id)
	picture = Response(recipient_id)
	if attachment != "":
		response.text = "Nice pic!"
	elif "dookie:" in message and str(recipient_id) in Admin_ID: #for adding custom messages
		con = getCon()
		add_custom_message(message_text, con)
		response.text = "Adding custom message..."
		con.close()

	elif "time" in message:
		response.text = getTime(message)

	elif checkForDino(message): #rename to checkfordino later
		value = checkForDino(message)
		con = getCon()
		response.text = getDino(message, value, recipient_id, con) #CURRENTLY CALLED checkForDino
		con.close()

		button = UrlButton("Latemeal","https://user.resi.inloop.com.au/home").get_button()
		response.addbutton(button)
		button = UrlButton("Leave Feedback","https://bit.ly/3hVT0DX").get_button()
		response.addbutton(button)

	elif checkForShopen(message, recipient_id):
		response.text = checkForShopen(message, recipient_id)

	elif checkForCalendar(message):
		response.text = checkForCalendar(message)

	elif checkForDay(message) or "tomorrow" in message or "today" in message or "all" in message:
		response.text = getDino(message, "breakfast", recipient_id)
		response.send()
		response.text = getDino(message, "lunch", recipient_id)
		response.send()
		response.text = getDino(message, "dinner", recipient_id)

		button = UrlButton("Latemeal","https://user.resi.inloop.com.au/home").get_button()
		response.addbutton(button)

	elif "latemeal" in message or "late" in message or "inloop" in message:
		response = "Order a late meal here:"
		button = UrlButton("Latemeal","https://user.resi.inloop.com.au/home").get_button()
		response.addbutton(button)

	elif "thx" in message or "thanks" in message or "thank you" in message or "thankyou" in message:
		response.text =  " ".join(["You're welcome!", u"\U0001F60B"]) #tongue out emoji

	elif "idiot" in message or "dumb" in message or "stupid" in message:
		link = Sender(recipient_id).get_profile_pic()
		picture.attachment = Image(link).get_image()
		picture.send()
		response.text = "This you?"

	elif "gif" in message:
		response.attachment = Gif("nice").get_gif()

	elif "joke" in message:
		response.text = getjoke()

	elif "show me users" in message:

		if str(recipient_id) in Admin_ID: 
			con = getCon()
			response.text = "Check the logs."
			print("Users: \n" + view_users(con))
			con.close()
		else:
			response.text = "You shall not, PASS: \n" + str(recipient_id)

	elif "hello" in message or "hey" in message or "help" in message or "hi" in message: #hi sometimes causes conflicts
		button = UrlButton("BssrBot Page","https://www.facebook.com/BssrBot-107323461505853/").get_button()
		#print(str(button) + " Button")
		response.addbutton(button)
		response.text = greeting_message
		#Response.addbutton(button)

	else:	
		try:
			reply = bot.reply(str(recipient_id), message)
			if reply == "As good as me.":
				link = Sender(recipient_id).get_profile_pic()
				picture.attachment = Image(link).get_image()
				picture.send()
				response.text = reply
			else:
				response.text = reply
		except:
			response.text = "'".join(["Sorry, I don't understand: ",message_text,""])
			PrintException()
	response.addquick_replies(dino_quickreplies)
	response.send()
	#--------------------------------------------------------------------------------------------------------------------------------------------------------
	return "Response formulated"

def getTime(message):
	response = ""
	if "baxter" in message:
		response = response + notbassertimes["Baxter"]
	elif "goldstein" in message or "goldie" in message or "goldy" in message:
		response = response + notbassertimes["Goldstein"]
	elif "fig" in message:
		response = response + notbassertimes["Fig"]
	elif "hall" in message:
		response = response + notbassertimes["Hall"]
	else:
		meal = checkForDino(message)
		if meal:
			if meal == "dino":
				response = response + dinotimes
			else:
				response = "".join([response, f"Basser {meal} is at ",bassertimes[meal],"."])
		else :
			response = response + dinotimes
	return response



def checkForDino(message):
        value = None
        if "dino" in message:
                value = "dino"
        elif "breakfast" in message or "breaky" in message or "brekky" in message:
                value = "breakfast"
        elif "lunch" in message:
                value = "lunch"
        elif "dinner" in message or "dins" in message or "supper" in message:
                value = "dinner"
        return value

def checkForShopen(message, recipient_id): #this can be mademore efficient
	user = Sender(recipient_id)
	name =  user.get_fullname()
	response = ""
	global shop_catalogue
	if shop_catalogue == None:
		#global shop_catalogue
		shop_catalogue = "No catalogue." + u"\U0001F4A9" #poop emoji
	if "i would like to open the shop" in message:
		con = getCon()
		response = response + open_shopen(name, con)
		con.close()
	elif "i would like to close the shop" in message:
		con = getCon()
		##add feature where only person who opened can close
		response = response + close_shopen(name, con)
		con.close()
	elif "shopen" in message or ("shop" in message and ("catalogue" not in message and "sell" not in message)):
		con = getCon()
		response = response + get_shopen(con)
		response = response + "\n" + "\n" + shop_catalogue
		con.close()
	elif "catalogue" in message or ("shop" in message and "sell" in message):
		response = response + str(shop_catalogue)
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


# def getResponse(entity, value, confidence):
# 	response = "blank"
# 	if entity == "Praise:Praise":
# 		response = f"No, you're {value}."
# 	return response
