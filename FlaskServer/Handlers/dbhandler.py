import datetime
import sqlite3
import config
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class DbHandler:

    def __init__(self):
        self.connection = sqlite3.connect(config.DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def create_user(self, username, password):
        password_hash = pwd_context.encrypt(password)
        createUserQuery = "INSERT INTO Users (username, password) VALUES('" + username + "', '" + password_hash + "')"
        if len(self.retreive_user(username)) >= 1:
            return "Username already exists"
        self.execute_query(createUserQuery)
        return "User created succesfully."

    def retreive_user(self, username):
        retreiveUserQuery = "SELECT * FROM Users WHERE username = '" + username + "';"
        user = self.fetch_result(self.execute_query(retreiveUserQuery))
        return user

    def retreive_router(self, router_id):
        retreiveRouterQuery = "SELECT router_id FROM Routers WHERE router_id = " + str(router_id) + ";"
        return self.fetch_result(self.execute_query(retreiveRouterQuery))

    def login_user(self, username, password):
        result = self.retreive_user(username)
        if len(result) == 0:
            return [(False, "Username does not exist")]
        if pwd_context.verify(password, result[0][2]) == True:
            token = self.generate_token(result[0][0], result[0][1])
            print (token)
            return [(True, token.decode('ascii'))]
        self.record_error(config.ERROR_LOGIN_ATTEMPT, "Attempt login on user: " + str(username))
        return [(False, "Incorrect password")]

    def generate_token(self, id, username, expiration = config.TOKEN_EXPIRE):
        s = Serializer(config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'username': username, 'id': id})

    def register_router(self, user_id, router_id):
        router = self.retreive_router(router_id)
        if len(router) == 0:
            self.record_error(config.ERROR_INVALID_ROUTER, "User attempted: " + str(user_id) + ", router does not exist: " + str(router_id) )
            return "Router not found"
        registerQuery = "INSERT INTO UserRouters (user_id, router_id) VALUES ( " + str(user_id) +", " + str(router_id) + " )"
        print(registerQuery)
        result = self.execute_query(registerQuery)
        if result == 0:
            self.record_error(config.ERROR_INVALID_ROUTER, "router already registered: " + str(router_id))
            return "router already registered"
        return "router registered"

    def init_router(self, router_id, router_address):
        checkRouter = "SELECT router_id FROM Routers WHERE router_id = " + str(router_id) + ";"
        result = self.fetch_result(self.execute_query(checkRouter))
        if len(result) == 0:
            self.record_error(config.ERROR_INVALID_ROUTER, "Invalid router init from: " + str(router_address) + "")
            return "Router does not exist"
        initRouterQuery = "UPDATE Routers SET router_address = '" + str(router_address) + "' WHERE router_id = " + str(router_id) + ";"
        self.execute_query(initRouterQuery)
        return "updated"

    def init_sensor(self, sensor_id, router_id):
        checkSensorExists = "SELECT sensor_id FROM Sensor WHERE sensor_id = " + str(sensor_id) + ";"
        result = self.fetch_result(self.execute_query(checkSensorExists))
        if len(result) == 0:
            self.record_error(config.ERROR_INVALID_SENSOR, "Router " + str(router_id) + " tried to register sensor: " + str(sensor_id) + ", does not exist")
            return "sensor does not exist"
        findSensor = "SELECT sensor_id FROM RouterSensors WHERE sensor_id = " + str(sensor_id) + ";"
        result = self.fetch_result(self.execute_query(findSensor))
        if len(result) >= 1:
            initSensorQuery = "UPDATE RouterSensors SET router_id = " + str(router_id) + " WHERE sensor_id = " + str(sensor_id) + ";"
            print("Updating sensors router")
        else:
            initSensorQuery = "INSERT INTO RouterSensors (sensor_id, router_id) VALUES (" + str(sensor_id) + ", " + str(router_id) + ");"
            print("Adding sensors router")
        self.execute_query(initSensorQuery)

    def get_router_sensors(self, router_id):
        findRouterSensor = "SELECT RouterSensors.sensor_id, Sensor.sensor_settings FROM RouterSensors INNER JOIN Sensor ON Sensor.sensor_id = RouterSensors.sensor_id WHERE RouterSensors.router_id = " + str(router_id) + ";"
        result = self.fetch_result(self.execute_query(findRouterSensor))
        print(result)
        return result

    def verify_auth_token(self, token):
        s = Serializer(config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return "Token expired"
        except BadSignature:
            return "Token does not exist"
        user = self.retreive_user(data.get("username",""))
        return bool(user)

    def get_user_from_token(self, token):
        s = Serializer(config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return "Token expired"
        except BadSignature:
            return "Token does not exist"
        user = self.retreive_user(data.get("username",""))
        return user

    def check_admin(self, username):
        adminQuery = "SELECT is_admin FROM Users WHERE username = '" + str(username) + "';"
        result = self.fetch_result(self.execute_query(adminQuery))[0][0]
        if result == False:
            self.record_error(config.ERROR_UNAUTHORISED_ACCESS, "User " + str(username) + ", tried to access admin domain")
        return True if result == 1 else False

    #TODO: Record Errors in Database
    def record_error(self, error_type, error_message):
        errorQuery = "INSERT INTO Errors (timestamp, error_type, error_message) VALUES ('" + str(datetime.datetime.utcnow()) + "', '" + str(error_type) + "', '" + str(error_message) + "');"
        print(errorQuery)
        self.execute_query(errorQuery)
        return

    def execute_query(self, query):
        result = []
        try:
            result = self.cursor.execute(query)
        except Exception as e:
            print (e)
            result = 0
        self.save()
        return result

    def save(self):
        """
        Saves the database after successful insertion/deletion
        """
        self.connection.commit()

    def close(self):
        """
        Closes db connection
        """
        self.cursor = None
        self.connection.close()

    @staticmethod
    def fetch_result(result):
        """
        Fetch query result into a python array.
        :param result: query result
        :return: result array
        """
        result_array = []
        while True:
            fetched_result = result.fetchone()
            if fetched_result is None:
                break
            result_array.append(fetched_result)
        return result_array