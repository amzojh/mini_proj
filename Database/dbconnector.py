import pymysql
import os
import pandas as pd

DATABASE_ENDPOINT = os.environ.get("DATABASE_ENDPOINT")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_DBNAME = os.environ.get("DATABASE_DBNAME")

class sqlConnector():
    
    def __init__(self):
        print(f"""
            DATABASE_DBNAME : {DATABASE_DBNAME}
            DATABASE_ENDPOINT : {DATABASE_ENDPOINT}
            DATABASE_PASSWORD : {DATABASE_PASSWORD}
            DATABASE_PORT : {DATABASE_PORT}
            DATABASE_USERNAME : {DATABASE_USERNAME}
            """)
        self.db = pymysql.connect(host=DATABASE_ENDPOINT, 
                            port=int(DATABASE_PORT), 
                            user=DATABASE_USERNAME, 
                            passwd=DATABASE_PASSWORD, 
                            db=DATABASE_DBNAME, 
                            charset="utf8")