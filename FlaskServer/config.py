from flask import request
from functools import wraps

DEBUG = True                        #Change to false if printing json requests is to be turned off
HOST = '127.0.0.1'                  #IP for the flask server to run on
SECRET_KEY = '123sdjk21239ska'      #Server secret key
DATABASE_NAME = 'database.sqlite3'  #Database name
TOKEN_EXPIRE = 9999

#Error types
ERROR_LOGIN_ATTEMPT = "lOGIN"
ERROR_INVALID_ROUTER = "INVRO"
ERROR_INVALID_SENSOR = "INVSE"
ERROR_UNAUTHORISED_ACCESS = "UAUTH"

def debug_method(f):
    """
    use as an @ below a @route for json to be printed
    """
    @wraps(f)
    def printDebug(*args, **kwargs):
        if DEBUG == True:
            print(request.json)
        return f(*args, **kwargs)
    return printDebug