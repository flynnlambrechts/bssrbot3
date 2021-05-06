def checkForEasterEggs(message):
    response = []

    if ("tall" in message or "height" in message) and ("sam" in message or "bensley" in message):
        if "really" in message:
            response.append("*cough* 5`11")
        else:
            response.append("6 foot")
    elif "room points" in message:
        response.append("Room points are a lie!")
    elif "bssrprdctns" in message or "basser productions" in message:
        response.append("Huge Content Coming Soon!")
    elif "dean" in message and "deputy" in message:
        response.append("THE DEPUTYYYY DEANNNNN")
        gif = "salute"
    elif "sam bensley" in message or "zoe bott" in message or "albert" in message:
        response.append("did you mean: 'sexy alpha coders'")
    elif "easter egg" in message:
        response.append("go find em")
        gif = "easter egg"
    elif "baxter" in message:
        response.append("Get rekt Baxter")
        gif = "get rekt"
    elif "goldstein" in message:
        response.append("Basser is better")
        gif = "dab"
    elif "baxtabot" in message:
        response.append("Do you mean: 'less inferior bot'?")
        gif = "sorry not sorry"
    elif "zali" in message or "president" in message:
        response.append("Madame president")
        gif = "donald trump"
    elif "matthew" in message or "batesy" in message or "bates" in message or "matt" in message or "batesos" in message:
        response.append("Daenerys of the House Targaryen, the First of Her Name, The Unburnt, Queen of the Andals, the Rhoynar and the First Men, Queen of Meereen, Khaleesi of the Great Grass Sea, Protector of the Realm, Lady Regent of the Seven Kingdoms, Breaker of Chains and Mother of Dragons")
        gif = "dracarys"
    elif "wam" in message and "jodie" in message:
        response.append("Higher than yours")
    elif "meme" in message:
        response.append("")
        gif = "meme"
    return response
