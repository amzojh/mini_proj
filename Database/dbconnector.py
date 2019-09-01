import pymysql
import os

DATABASE_ENDPOINT = os.environ.get("DATABASE_ENDPOINT")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_DBNAME = os.environ.get("DATABASE_DBNAME")

class sqlConnector():
    
    def __init__(self):
        print(DATABASE_DBNAME, DATABASE_ENDPOINT, DATABASE_PASSWORD, DATABASE_PASSWORD, DATABASE_PORT, DATABASE_USERNAME)
        db = pymysql.connect(host=DATABASE_ENDPOINT, port=DATABASE_PORT, user=DATABASE_USERNAME, passwd=DATABASE_PASSWORD, charset='utf-8', db=DATABASE_DBNAME)