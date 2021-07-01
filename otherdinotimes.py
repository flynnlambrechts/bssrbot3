#other dino times

def notBasser(message):
	response = ""
	if "baxter" in message and "time" in message:
		response = response + "Baxter Dino Times:\nBreakfast: 8:00-8:45am\nLunch: 12:45-1:30pm\nDinner: 5:45-6:30pm"
	elif ("goldstein" in message or "goldie" in message or "goldy" in message) and "time" in message:
		response = response + "Goldstein Dino Times:\nBreakfast: 9:00-9:45am\nLunch: 1:45-2:30pm\nDinner: 6:45-7:30pm"
	elif "fig" in message and "time" in message:
		response = response + "Fig Tree Dino Times:\nBreakfast: 9:00-9:45am\nLunch: 1:45-2:30pm\nDinner: 6:45-7:30pm"
	elif "hall" in message and "time" in message:
		response = response + "Hall Dino Times:\nBreakfast: As Normal \nDinner: 7:45-8:30pm"
	return response
	