#response
from bot_constants import ACCESS_TOKEN
import requests
import json

class Response:
	def __init__(self,recipient_id,text=None,attachment=None):
		self.recipient_id = recipient_id

		self.text = text
		self.attachment = attachment
		self.quick_replies = []

		self.buttons = []
		
	def addbutton(self,button): #requires individual dictionaries
		self.buttons.append(button)

	def addquick_replies(self,quick_replies): #requires a list of dictionaries
		self.quick_replies = quick_replies

	def send(self):
		recipient_id = self.recipient_id
		params = {
		   "access_token": ACCESS_TOKEN
		}

		headers = {
			"Content-Type": "application/json"
		}

		if self.attachment != None:
			data = {
		    	"recipient": {"id": recipient_id},
		    	"message": {
		            "attachment": self.attachment
            	}
			}
		else: #must be text
			if self.buttons != []:
				data = {
					"recipient": {"id": recipient_id},
					"message": {
						"attachment":{
							"type":"template",
							"payload":{
								"template_type":"button",
								"text": self.text,
								"buttons": self.buttons
							}
						}
					}
				}
			else: #No buttons
				data = {
					"recipient": {"id": recipient_id},
					"message": {
						"text": self.text}
				}

		if self.quick_replies != []:
			data["message"]["quick_replies"] = self.quick_replies #a list

		data = json.dumps(data)
		#print(data)
		r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)



class Button:
	def __init__(self,title):
		self.title = title


class UrlButton(Button):
	def __init__(self,title,url):
		super().__init__(title)
		self.url = url
		self.button = {
			"type": "web_url",
			"url": self.url,
			"title": self.title
			}

	def get_button(self):
		return self.button


class QuickReply:
	def __init__(self,title,payload):
		self.title = title
		self.payload = payload
		#self.image = None

	def get_quickreply(self):
		quickreply = {
				"content_type":"text",
				"title":self.title,
				"payload":self.payload
				}
		return quickreply


class Gif:
	def __init__(self,text):
		self.gifurl = self.search_gif(text)

	def search_gif(self,text):
		payload = {'s': text, 'api_key': 'ey1oVnN1NGrtEDHFGBJjRj5AgegLFVeT', 'weirdness': 1}
		r = requests.get('http://api.giphy.com/v1/gifs/translate', params=payload)
		r = r.json()
		# sprint(r)
		try:
			url = r['data']['images']['original']['url']
		except:
			print('failed to get gif')

		return url

	def get_gif(self):
		self.attachment = {
		"type": "image",
		"payload": {
			"url": self.gifurl}
		}
		return self.attachment

class Image:
	def __init__(self,url):
		self.imageurl = url

	def get_image(self):
		self.attachment = {
		"type": "image",
		"payload": {
			"url": self.imageurl}
		}
		return self.attachment





