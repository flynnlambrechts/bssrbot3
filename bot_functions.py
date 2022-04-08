# Bot Functions
import os
import sys
import psycopg2
from datetime import *
from linecache import (checkcache, getline)  # for error handling

from bot_constants import (DATABASE_URL, TIMEZONE)
# from models import GlobalVar


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    checkcache(filename)
    line = getline(filename, lineno, f.f_globals)
    print(
        f'EXCEPTION IN ({filename}, LINE {lineno} "{line.strip()}"): {exc_obj}')


def getCon():  # gets the connection  to the database when required
    if "HEROKU" in os.environ:
        DATABASE_URL = os.environ['DATABASE_URL']
        con = psycopg2.connect(DATABASE_URL, sslmode='require')
    else:
        con = psycopg2.connect(database="bssrbot1", user="flynnlambrechts",
                               password="", host="127.0.0.1", port="5432")
        print("Local Database opened successfully")
    return con

# def daysuntil(day): #date provided in date(YYYY,M,D) format
#     today = date.today()
#     diff = day - today
#     return (diff.days)


def daysuntil(future):  # date provided in date(YYYY,M,D) format
    today = int(datetime.now(TIMEZONE).strftime('%j'))
    return int(future.strftime('%j')) - today
