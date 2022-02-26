#dinovote

#gonna need to prevent users from voting more than once so make a list of users who have voted for each meal
#also gonna need to use same times for each dino meal
#also add buttons for voting
#maybe add quick reply to check vote
#make the table
#table: day:, meal:, votes for good:, votes for bad:, users who have voted(maybe new table)

def getvote(meal, value): #as a percentage of good or bad depending of what is higher
	vote = {}
	if meal == "breakfast":
		vote["breakfast"] = value
	elif meal == "lunch":
		vote["lunch"] = value
	elif meal == "dinner":
		vote["dinner"] = value
	vote.get("breakfast") #outputs None if no breafast value
	return vote

def addvote(vote, con):
	try:
		date = str(datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d'))
		cur = con.cursor()
		dummy = ""
		vote = getvote(meal)

		cur.execute('''SELECT EXISTS (SELECT day FROM custom_message WHERE day = %s)''', (date,))
		#check if current day exists
		dummy = str(cur.fetchone())
		print(dummy + " dummy")
		if dummy != "(False,)": #if the day exits then update current day
			print("updating todays vote")
			cur.execute('''UPDATE dinovote SET
			breakfast = breakfast+COALESCE(%s,0)
			lunch = lunch+COALESCE(%s,0),
			dinner = dinner+COALESCE(%s,0)
			WHERE day = %s''',(vote.get("breakfast"),vote.get("lunch"),vote.get("dinner"),date))

		else: #otherwise overwrite previous day with blank values
			print("overwriting previous day")
			cur.execute('''UPDATE dinovote SET
			day = %s, breakfast = 0, lunch = 0,
			dinner = 0''', (date))

			print("adding todays vote")
			cur.execute('''UPDATE dinovote SET
			breakfast = breakfast+COALESCE(%s,0)
			lunch = lunch+COALESCE(%s,0),
			dinner = dinner+COALESCE(%s,0)
			WHERE day = %s''',(vote.get("breakfast"),vote.get("lunch"),vote.get("dinner"),date))



	except Exception as error:
		print("Error in addvote" + str(error) + "\n" + str(type(error)))

def readvote(meal, con):
	try:
		date = str(datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d'))
		cur = con.cursor()
		cur.execute('''SELECT meal FROM dinovote WHERE day = %s AND meal = %s''',(date, meal))
		value = cur.fetchone()
		print(value)
		reponse = "Vote read"

	except Exception as error:
		response = "No one has voted for dino today..."
		print("Error in readvote" + str(error) + "\n" + str(type(error)))

	return response

