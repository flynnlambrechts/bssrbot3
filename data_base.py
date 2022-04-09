import psycopg2

from bot_constants import DATABASE_URL
# from models import GlobalVar

def getCon():  # gets the connection  to the database when required
    # if "HEROKU" in os.environ:
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    return con

global con
con = getCon()