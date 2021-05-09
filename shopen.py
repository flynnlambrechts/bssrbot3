import os
import psycopg2

import time
import datetime
import pytz

TIMEZONE = pytz.timezone('Australia/Sydney')

from connectdb import connectToDB
from connectdb import con
global con   

global person
person = str("Mike Hunt")

global index
index = int(1)

global current_time, end_time, date
'''
current_time = datetime.datetime.now(TIMEZONE).strftime('%H:%M:%S')
date_and_time = datetime.datetime.now(TIMEZONE)
end_time = (date_and_time + datetime.timedelta(hours=3)).strftime('%H:%M:%S') #closes shop after 3 hours
'''

date_and_time = datetime.datetime.now(TIMEZONE)
current_time = datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
end_time = (date_and_time + datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
date = str(datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d'))


def create_shopen():
    global con
    cur = con.cursor()
    response = ""
    try: 
        cur.execute('''CREATE TABLE shopen1
            (index INTEGER NOT NULL PRIMARY KEY,
            person VARCHAR(50) NOT NULL,
            start_time VARCHAR(50) NOT NULL,
            end_time VARCHAR(50) NOT NULL,
            value BOOLEAN NOT NULL,
            date DATE NOT NULL)
            ''')
        print("Table created successfully")
        response = response + "Table created."
        con.commit()
    except Exception as error:
        response = response + "Fail: " + str(error)
        print("Error: " + str(error) + "\n" + str(type(error)))
    return response

def insert_shopen():
    global con
    global person
    global index
    global current_time, end_time, date
    response = ""
    try:
        cur = con.cursor()
        cur.execute('''INSERT INTO shopen1 (
            index, person, start_time, end_time, value, date)
            VALUES (%s,%s,%s,%s,%s,%s)''',
                (index, person,current_time,end_time,'true',date))
        print("Shopen data inserted successfully")
        response  = response + "Shop row inserted"
        con.commit()
    except Exception as error:
        response = response + "Fail: " + str(error)
        print("Error: " + str(error) + "\n" + str(type(error)))
    return response


def open_shopen(name):
    try: 
        global con
        global index
        global current_time, end_time, date
        cur = con.cursor()
        cur.execute('''UPDATE shopen1 SET
            index=%s, person= %s, start_time = %s, end_time = %s, value = %s,
            date = %s''',
                (index,name,current_time,end_time,'true',date))
        print("Shopen updated successfully")
        con.commit()
        return "Shop has been opened! \nShop will be automatically closed in 3hours."
    except Exception as error:
        print("Error: " + str(error) + "\n" + str(type(error)))
        return "Fail: " + str(error)

def close_shopen(name):
    try:
        global con
        global index
        unix = int(time.time())
        current_time = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        cur = con.cursor()
        cur.execute('''UPDATE shopen1 SET
            index=%s, person= %s, end_time = %s, value = %s''',
                (index, name, current_time,'false'))
        print("Shopen updated successfully")
        con.commit()
        return "Shop has been closed!"
    except Exception as error:
        print("Error: " + str(error) + "\n" + str(type(error)))
        return "Fail: " + str(error)
        

def timeTillClose(end_time):
    current_time = datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
    close_time = datetime.datetime.strptime(str(end_time),'%Y-%m-%d %H:%M:%S')
    remaining_time = close_time - datetime.datetime.strptime(str(current_time),'%Y-%m-%d %H:%M:%S')
    return remaining_time

def get_shopen():
    try:
        global con
        cur = con.cursor()
        cur.execute('''SELECT * FROM shopen1''')
        rows = cur.fetchall()
        response = ""
        for row in rows:
            '''
            print("person =", row[0])
            print("start_time =", row[1])
            print("end_time =", row[2])
            print("value =", row[3])
            print("date =", row[4], "\n")
            '''
            person = str(row[1])
            start_time_string = row[2]
            start_time = datetime.datetime.strptime(str(start_time_string),'%Y-%m-%d %H:%M:%S')
            end_time_string = row[3]
            end_time = datetime.datetime.strptime(str(end_time_string),'%Y-%m-%d %H:%M:%S')
            value = str(row[4])
            date = row[5]
        
        if timeTillClose(end_time) >= datetime.timedelta(minutes=0):
            if value == "True":
                response = response + "Yes, shop was opened by " + person + " at " + str(start_time.strftime('%I:%M %p')) + "."
            elif value == "False":
                response = response + "Sorry, shop closed :("
        else:
            response = response + "Sorry, shop closed :("
    except Exception as error:
        print("Error: " + str(error) + "\n" + str(type(error)))
        response = ""
        response = response + "Fail: " + str(error)
    return response



