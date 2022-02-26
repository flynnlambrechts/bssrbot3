#Bot Functions
import os, sys
import psycopg2
from datetime import *
from linecache import (checkcache, getline) # for error handling

from bot_constants import (DATABASE_URL, Admin_ID, TIMEZONE)
from response import Response
# from models import GlobalVar

def PrintException(): #Prints Error messaged used in many places 
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    checkcache(filename)
    line = getline(filename, lineno, f.f_globals)
    print(f'EXCEPTION IN ({filename}, LINE {lineno} "{line.strip()}"): {exc_obj}')
    for ID in Admin_ID:
            response = Response(ID)
            response.text = "Oh no something went wrong :("
            response.send()


def getCon(): #gets the connection to the database when required
    if "HEROKU" in os.environ:
        DATABASE_URL =  os.environ['DATABASE_URL']
        con = psycopg2.connect(DATABASE_URL, sslmode='require')
    else:
        con = psycopg2.connect(database="bssrbot1", user="flynnlambrechts", password="", host="127.0.0.1", port="5432")
        print("Local Database opened successfully")
    return con

# def days_until(future): #date provided in date(YYYY,M,D) format
#     today = date.today()
#     diff = future - today
#     return (diff.days)

def days_until(future): #date provided in date(YYYY,M,D) format
    today = int(datetime.now(TIMEZONE).strftime('%j'))
    return int(future.strftime('%j')) - today