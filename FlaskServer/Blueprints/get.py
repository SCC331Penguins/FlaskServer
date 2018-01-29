from flask import request, jsonify, abort, Blueprint
from Handlers.dbhandler import DbHandler

get = Blueprint('get',__name__)

@get.route('/login', methods=['GET'])
def login():
    username = request.json['username']
    password = request.json['password']
    print(request.json)
    dbHandler = DbHandler()
    #username = dbHandler.retreive_user(username)

    print (dbHandler.retreive_user("StoutyA", "dredd"))

    return jsonify(message="Logged in: " + message), 201