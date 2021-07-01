
#### THIS NEEDS TO BE CLEANED THE HELL UP #####

#wit.ai
#watch https://www.youtube.com/watch?v=e29Aj6tJ_5k&list=PLyb_C2HpOQSC4M3lzzrql7DSppTeAxh-x&index=9
#and previous video in this playlist to understand

#from wit import Wit 
import time

#wit_access_token = "LZANSEIRATV3RJ7XZPP3TFIKUND427V6"

#client = Wit(access_token = wit_access_token)

#collects what the entity is e.g. mealtype
# and its value e.g. breakfast, lunch or dinner
def wit_response(message): #prev message_text
        #start = time.time()
        # resp = client.message(message) #prev message_text
        # #global entity
        # #global value
        entity = None
        value = None

        # try:
        #         entity = list(resp['entities'])[0]
        #         value = resp['entities'][entity][0]['value']
        # except:
        #         pass
        # 

        if "dino" in message:
                value = "dino"
        elif "breakfast" in message or "breaky" in message or "brekky" in message:
                value = "breakfast"
        elif "lunch" in message:
                value = "lunch"
        elif "dinner" in message or "dins" in message or "supper" in message:
                value = "dinner"
        if value is not None:
                entity = 'mealtype:mealtype'
        #end = time.time()
        #print(end - start)
        return (entity, value)

#test for random question:

'''
print(wit_response("what is breakfast"))
print(entity)
print(value)
'''
