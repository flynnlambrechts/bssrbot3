
import psycopg2

import time
import datetime
from pytz import timezone

TIMEZONE = timezone('Australia/Sydney')

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


def open_shopen(name, con):
    try: 
        global index
        date_and_time = datetime.datetime.now(TIMEZONE)
        current_time = datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
        end_time = (date_and_time + datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
        date = str(datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d'))
        cur = con.cursor()
        cur.execute('''UPDATE shopen1 SET
            index=%s, person= %s, start_time = %s, end_time = %s, value = %s,
            date = %s''',
                (index,name,current_time,end_time,'true',date))
        con.commit() #
        print("Shopen updated successfully") #
        return "Shop has been opened! \nShop will be automatically closed in 3hours."
    except Exception as error:
        print("Error: " + str(error) + "\n" + str(type(error)))
        return "Fail: " + str(error)

def close_shopen(name, con):
    try:
        global index
        global TIMEZONE
        current_time = datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
        cur = con.cursor()
        cur.execute('''UPDATE shopen1 SET
            index=%s, person= %s, end_time = %s, value = %s''',
                (index, name, str(current_time),'false'))
        print("Shopen updated successfully")
        con.commit()
        return "Shop has been closed!"
    except Exception as error:
        print("Error: " + str(error) + "\n" + str(type(error)))
        return "Fail: " + str(error)
        

def timeTillClose(end_time):
    current_time = datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
    close_time = datetime.datetime.strptime(str(end_time),'%Y-%m-%d %H:%M:%S')
    remaining_time = (close_time.timestamp()) - (datetime.datetime.strptime(str(current_time),'%Y-%m-%d %H:%M:%S').timestamp()) #
    print(str(remaining_time)) #
    return remaining_time

def get_shopen(con):
    try:
        cur = con.cursor()
        #this can be sped up without the for
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
        
        if int(timeTillClose(end_time)) >= 0:
            if value == "True":
                response = response + "Shop was opened by " + person + " at " + str(start_time.strftime('%I:%M %p')) + "."
            elif value == "False":
                response = response + "Sorry, shop closed " + u"\U0001F61E"
        else:
            response = response + "Sorry, shop closed " + u"\U0001F61E"
    except Exception as error:
        print("Error: " + str(error) + "\n" + str(type(error)))
        response = ""
        response = response + "Fail: " + str(error)
    return response




##def create_shopen(con):
##    response = ""
##    try: 
##        cur.execute('''CREATE TABLE shopen1
##            (index INTEGER NOT NULL PRIMARY KEY,
##            person VARCHAR(50) NOT NULL,
##            start_time VARCHAR(50) NOT NULL,
##            end_time VARCHAR(50) NOT NULL,
##            value BOOLEAN NOT NULL,
##            date DATE NOT NULL)
##            ''')
##        print("Table created successfully")
##        response = response + "Table created."
##        con.commit()
##    except Exception as error:
##        response = response + "Fail: " + str(error)
##        print("Error: " + str(error) + "\n" + str(type(error)))
##    return response
##
##def insert_shopen():
##    global person
##    global index
##    global current_time, end_time, date
##    
##    
##    response = ""
##    try:
##        cur = con.cursor()
##        cur.execute('''INSERT INTO shopen1 (
##            index, person, start_time, end_time, value, date)
##            VALUES (%s,%s,%s,%s,%s,%s)''',
##                (index, person,current_time,end_time,'true',date))
##        print("Shopen data inserted successfully")
##        response  = response + "Shop row inserted"
##        con.commit()
##    except Exception as error:
##        response = response + "Fail: " + str(error)
##        print("Error: " + str(error) + "\n" + str(type(error)))
##    return response


