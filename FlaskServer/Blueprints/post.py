from flask import request, jsonify, abort, Blueprint
from Handlers.dbhandler import DbHandler
from functools import wraps
import config

post = Blueprint('post',__name__)

def requires_token(f):
    """
    Wrap method to say that a route or method requires token authentication to continue
    :return: boolean
    """
    @wraps(f)
    def token_check(*args, **kwargs):
        token = request.json['token']
        dbHandler = DbHandler()
        if jsonify(user=dbHandler.verify_auth_token(token)) == False:
            return jsonify(message="Token invalid")
        return f(*args, **kwargs)
    return token_check

def requires_admin(f):
    @wraps(f)
    def admin_check(*args, **kwargs):
        dbHandler = DbHandler()
        user = dbHandler.get_user_from_token(request.json['token'])[0][1]
        admin = dbHandler.check_admin(user)
        if admin == False:
            return jsonify(result="You do not have access to this...")
        return f(*args, **kwargs)
    return admin_check


@post.route('/register', methods=['POST'])
@config.debug_method
def register():
    """
    Register a new user
    requires username and password
    :return: json (message(text))
    """
    username = request.json['username']
    password = request.json['password']
    dbHandler = DbHandler()
    message = dbHandler.create_user(username, password)
    return jsonify(message=message), 201

@post.route('/login', methods=['POST'])
@config.debug_method
def login():
    """
    Logs in as a user.
    requires a username and password
    :return: json (logged_in(boolean), token(text) or message(text) if logged_in is false)
    """
    username = request.json['username']
    password = request.json['password']
    dbHandler = DbHandler()
    result = dbHandler.login_user(username, password=password)
    if result[0][0] == True:
        return jsonify(logged_in=result[0][0], token=result[0][1]), 201
    return jsonify(logged_in=result[0][0], message=result[0][1]), 201

@post.route('/router/register', methods=['POST'])
@config.debug_method
@requires_token
def set_user_router():
    """
    Sets router for a user
    Requires a token and a router identifier
    :return: json (message(text), registered(boolean))
    """
    db = DbHandler()
    user = db.get_user_from_token(request.json['token'])
    router_id = request.json['router_id']
    return jsonify(result=db.register_router(user[0][0],router_id))

@post.route('/router/init', methods=['POST'])
@config.debug_method
def init_router():
    """
    Router calls this on start, sends router id and ip address
    :return: json (init(bool))
    """
    db = DbHandler()
    router_id = request.json['router_id']
    router_address = request.json['router_address']
    result = db.init_router(router_id, router_address)
    return jsonify(result=result)

@post.route('/sensor/init', methods=['POST'])
@config.debug_method
def init_sensor():
    """
    Init a sensor to a router
    :return: json (init(bool))
    """
    db = DbHandler()
    sensor_id = request.json['sensor_id']
    router_id = request.json['router_id']
    result = db.init_sensor(sensor_id, router_id)
    return jsonify(result=result)

@post.route('/router/get_sensors', methods=['POST'])
@config.debug_method
def get_router_sensors():
    db = DbHandler()
    router_id = request.json['router_id']
    result = db.get_router_sensors(router_id)
    return jsonify(result=result)

@post.route('/admin/errors', methods=['POST'])
@config.debug_method
@requires_token
@requires_admin
def get_errors():
    return jsonify(result="worked")