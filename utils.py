
#wit.ai
#watch https://www.youtube.com/watch?v=e29Aj6tJ_5k&list=PLyb_C2HpOQSC4M3lzzrql7DSppTeAxh-x&index=9
#and previous video in this playlist to understand

from wit import Wit 

wit_access_token = "LZANSEIRATV3RJ7XZPP3TFIKUND427V6"

client = Wit(access_token = wit_access_token)

#collects what the entity is e.g. mealtype
# and its value e.g. breakfast, lunch or dinner
def wit_response(message): #prev message_text
	resp = client.message(message) #prev message_text
	
	entity = None
	value = None

	try:
		entity = list(resp['entities'])[0]
		value = resp['entities'][entity][0]['value']
	except:
		pass

	return (entity, value)

#test for random question:
#print(wit_response("what is breakfast"))
