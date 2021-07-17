#first attempts using classes
import os
import requests

from users import insert_user
from bot_functions import (PrintException, getCon)

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


class GlobalVar:
	def __init__(self, name):
		self.name = name

	def insert(self, columns):
		try:
			self.columns = "(" + (", ".join(columns)) + ")"
			self.values = tuple(columns.values())

			con = getCon()
			cur = con.cursor()
			print('''INSERT INTO %s %s VALUES %s''' % (self.name, self.columns, self.values))
			con.commit()
			con.close()
		except:
			PrintException()

	def update(self, columns):
		try:
			self.columns = r" = '%s', ".join(columns) + r" = '%s'" #quotes around %s as these will ensure postgresql recieves them as strings and not columns
			self.values = tuple(columns.values())

			con = getCon() 
			cur = con.cursor()
			cur.execute('''UPDATE %s SET %s''' % (self.name, self.columns % self.values))
			con.commit()
			con.close()
			return f"{self.name} updated successfully."
		except:
			PrintException()	

	def get(self):
		try:
			con = getCon()
			cur = con.cursor()
			cur.execute(f'''SELECT * FROM {self.name}''')
			row = cur.fetchone()
			con.close()
			print(row)
			return row
		except:
			PrintException()