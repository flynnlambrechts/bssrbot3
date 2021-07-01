#users
import psycopg2



def insert_user(full_name, first_name, last_name, PSID, con):
    #global con 
    #con                                                             #CONNECT DB

    response = ""
    try:
        cur = con.cursor()
        cur.execute('''INSERT INTO users (
            full_name,
            first_name,
            last_name,
            PSID)
            VALUES (%s,%s,%s,%s)
            ON CONFLICT DO NOTHING''', (full_name, first_name, last_name, str(PSID)))
        #print("User data for " + first_name + " inserted successfully")
        con.commit()
    except Exception as error:
        #response = response + "Fail in insert user: " + str(error)
        print("User may be already added: " + str(error) + " type: " + str(type(error)))
    #con.close()                                                     #DISCONNECT DB


def view_users(con):
    #global con 
    #con                                                             #CONNECT DB

    response = ""
    try: 
        cur = con.cursor()
        cur.execute('''SELECT * FROM users''')
        rows = cur.fetchall()
        for row in rows:
            print("full_name =", row[0])
            full_name = str(row[0])
            print("first_name =", row[1])
            first_name = str(row[1])
            print("last_name =", row[2])
            last_name = str(row[2])
            print("PSID =", row[3], "\n")
            PSID = str(row[3])
            response = response + full_name + ", " + first_name + ", " + last_name + ", " + PSID + "\n"
    except Exception as error:
        if str((error)) == "connection already closed":
            response = response + "con closed"
        else:
            print("Error in Viewing Users: \n" + str(error) + " type: " + str(type(error)))
    #con.close()                                                     #DISCONNECT DB
    return response


# def create_users():
#    global con 
#    con                                                             #CONNECT DB

#    cur = con.cursor()
#    response = ""
#    try:
#        cur.execute('''CREATE TABLE users (
#            full_name VARCHAR(100) PRIMARY KEY NOT NUll,
#            first_name VARCHAR(50) NOT NULL,
#            last_name VARCHAR(50) NOT NULL,
#            PSID VARCHAR(200) NOT NULL 
#            ) ON CONFLICT DO NOTHING''')
#        print("User Table created successfully")
#        con.commit()
       
#    except Exception as error:
#        response = response + "Fail in adding users table: " + str(error)
#        print("Error: " + str(error) + "\n" + str(type(error)))
#    con.close()                                                     #DISCONNECT DB
#    return response

