#Coffee Night Stuff
#Wildcat Nominations
#Quote Nominations
#Photos
import datetime
from dateutil.relativedelta import relativedelta, WE
from tabulate import tabulate
#from github import Github
import github

from bot_constants import (TIMEZONE, PAT)
from bot_functions import (getCon, PrintException)

from models import Sender

# https://medium.com/geekculture/files-on-heroku-cd09509ed285
github = github.Github(PAT)
repository = github.get_user().get_repo('bssrbot-dev') #maybe make so this knows whether its in bssrbot or bssrbot-dev

# Getting qutoes or wildcat nominations
# Inputing into here is done through rive_reply.py
def get_coffee(item): #item is either quotes or wildcats
	try:
		date = datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d')
		start_date = datetime.datetime.now(TIMEZONE) + relativedelta(weekday=WE(-1)) #Finds date of last coffee night (assuming it's wednesday)
		#print(start_date)

		con = getCon()
		cur = con.cursor()
		cur.execute(f'''SELECT * FROM {item} WHERE date >= '{start_date}'::DATE''') #change this to the previous coffee night
		rows = cur.fetchall()

		# path in the repository
		filename = f'coffee_{item}.html'

		#f = open(f"coffee_{item}_{date}.txt", "w+")
		#result = f"{date} --- {item}\n"
		table = [["Nominee","Reason/Quote","Date","Nominator"]]
		for row in rows:
			table.append(list(row))
			#result = result + f"{row[0]} | {row[1]} | {row[2]} | {row[3]}\n"
			#print(row)

		content = tabulate(table, tablefmt='html')

		con.close()

		# create with commit message
		try: #potentially flip the order of these two
			repository.create_file(filename, f"Coffee Night {item}", content)
		except:
			print("Create Failed, Trying updating instead")
			file = repository.get_contents(f"{filename}")
			contents = repository.get_contents("")
			repository.update_file(filename, f"Coffee Night {item}",content, file.sha)

		file_path = str(filename) #the filepath
		return file_path
	except:
		PrintException()




#--- Photo Submission
