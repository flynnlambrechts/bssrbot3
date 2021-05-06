def checkForEasterEggs(message):
    response = ""
    if "updog1" in message:
        response = response + "Room points are a lie!")
    elif message == "random":
        sample_responses = ["ben is a cockboy","molly farted","crispy is a simp","mitchy is thick","hugo is sick"]
        response = response + random.choice(sample_responses)
    return response
