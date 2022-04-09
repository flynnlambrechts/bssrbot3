'''CREATE TABLE images (
day VARCHAR(20) NOT NULL PRIMARY KEY,
breakfast text[],
lunch text[],
dinner text[]
);'''

from datetime import datetime
from bot_constants import TIMEZONE
from bot_functions import getCon

def date():
    return str(datetime.now(TIMEZONE).strftime('%Y-%m-%d'))

def pick_meal():
    meal = ""
    time = datetime.now(TIMEZONE).time().hour
    if time < 10:
        meal  = "breakfast"
    elif time < 14:
        meal = "lunch"
    else:
        meal = "dinner"
    return meal

def add_dino_image(url, con):
    breakfast = None
    lunch = None
    dinner = None

    meal = pick_meal()

    date = date()

    cur = con.cursor()
    cur.execute('''SELECT EXISTS (SELECT day FROM images WHERE day = %s)''', (date,))
    dummy = str(cur.fetchone())

    if dummy != "(False,)":
        #make so only updates specific row instead of all rows
        cur.execute(f"""UPDATE images SET
        {meal} = array_append({meal}, '{url}') WHERE day = '{date}'""")
        con.commit()
        print("custom_message updated successfully")
    
    else: #otherwise add new row with the current date
        print("adding row")
        cur.execute('''INSERT INTO images(
            day, breakfast, lunch, dinner)
            VALUES (%s,%s,%s,%s)''', 
            (date, breakfast, lunch, dinner,))
        con.commit()
        print("row added successfully")
        add_dino_image(url, con)


def get_dino_image(meal, con):
    date = date()

    try:
		cur = con.cursor()
		cur.execute('''SELECT * FROM images WHERE day = %s''',(date,))
		row = cur.fetchone()
        meal = pick_meal()

		if meal == 'breakfast' and row[1] is not None:
			urls = (row[1])
		elif meal == 'lunch' and row[2] is not None:
			urls = (row[2])
		elif meal == 'dinner' and row[3] is not None:
			urls = (row[3])

	except TypeError:
			#PrintException()
			print("Type Error in read_custom_message: Probably no message.")
			pass
	except:
			PrintException()
	return urls