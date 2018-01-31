from flask import request
from functools import wraps

DEBUG = True                        #Change to false if printing json requests is to be turned off
HOST = '127.0.0.1'              #IP for the flask server to run on
SHARED_SECRET_KEY = 'scc331sharedsecretkey'      #Server secret key
DATABASE_NAME = 'database.sqlite3'  #Database name
TOKEN_EXPIRE = 999999

#Error types
ERROR_LOGIN_ATTEMPT = "lOGIN"
ERROR_INVALID_ROUTER = "INVRO"
ERROR_INVALID_SENSOR = "INVSE"
ERROR_UNAUTHORISED_ACCESS = "UAUTH"