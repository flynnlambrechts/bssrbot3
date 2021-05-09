#connect DB
import os
import psycopg2

def connectToDB():
    global con
    ENV = "HEROKU"
    if ENV == "LOCAL":
        con = psycopg2.connect(database="bssrbot1", user="flynnlambrechts", password="", host="127.0.0.1", port="5432")
        print("Local Database opened successfully")
    if ENV == "HEROKU":
        DATABASE_URL =  os.environ['DATABASE_URL']
        con = psycopg2.connect(DATABASE_URL, sslmode='require')
    else:
        print("ENV specified wrong.")

connectToDB()
#con.close()
