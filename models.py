#first attempts using classes
import os
import requests

from users import insert_user

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

class Sender:
	def __init__(self, recipient_id):
		URL = "".join(["https://graph.facebook.com/v2.6/", recipient_id, "?fields=first_name,last_name,profile_pic&access_token=", ACCESS_TOKEN])
		r = requests.get(url = URL)
		data = r.json()
		self.first_name = data['first_name']
		self.last_name = data['last_name']
		self.psid = recipient_id
		self.full_name  = " ".join([data['first_name'],data['last_name']])
		self.profile_pic = data['profile_pic']

	def get_firstname(self):
		return self.first_name

	def get_lastname(self):
		return self.last_name

	def get_fullname(self):
		return self.full_name

	def get_profile_pic(self):
		return self.profile_pic

	def adduser(self, con):
		insert_user(self.full_name, self.first_name, self.last_name, self.psid, con)


# user = Sender(recipient_id)
# print(user.get_fullname())