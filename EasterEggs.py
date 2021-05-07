import random

def checkForEasterEggs(message):
    response = ""
    if "updog" in message:
        response = response + "What is updog?"
    elif message == "random":
        sample_responses = ["ben is a cockboy","molly farted","crispy is a simp","mitchy is thick","hugo is sick"]
        response = response + random.choice(sample_responses)
    elif "molly" in message or "molly rolfe" in message or "rolfey" in message:
        response = response + "Molly is a butt nug."
    elif "benny g" in message or "ben grant" in message:
        response = response + "Time for the bad man to settle down..."
    elif "crispy" in message or "brendan crisp" in message:
        response = response + "That man is bricked up in a brick house."
    elif "feature" in message:
        response = response + "Come to 507 if you want a feature."
    elif "hugo" in message or "hugo john" in message:
        response = response + "A really commited vego most likely with a hickey on his neck."
    elif "mitch" in message or "mitch kerrison" in message or "mitchy" in message:
        response = response + "Did you mean: 'Booty Mitch'?"
    elif "flynn" in message or "flynn lambrechts" in message:
        response = response + "Sick Lad"    
    elif "mackenzie" in message or "mackenzie travers" in message or "kenz" in message:
        response = response + "Hey gang member..."
    elif "dumptruck" in message or "dumpy" in message:
        response = response + "Did you mean 'Mitch Kerrison'?"
    elif "507" in message:
        response = response + "The best fresher box in town."
    elif "baxter" in message:
        response  = response  + "Get rekt Baxter."
    elif "goldstein" in message:
        response  = response  + "Basser is better."
    elif "baxtabot" in message:
        response =  response + "Did you mean: 'inferior bot'?"
    elif "room points" in message:
        response  = response  + "Room points are a lie!"
    elif "floor 1" in message or "floor one" in message:
        response  = response  + "The dungeon..."
    elif "floor 5" in message or "floor five" in message:
        response  = response  + "Penthouse baby!!"
    elif "joe" in message:
        response  = response  + "Who's Joe?"
    elif "can you hold my basketball" in message or "can you look after my basketball":
        response  = response  + "Okay Benny G with the smooth moves."
    elif "em col" in message:
        response  = response  + "Hold my bball?"
    elif "floor 4" in message or "floor five" in message::
        response  = response  + "the second best floor"
    return response
