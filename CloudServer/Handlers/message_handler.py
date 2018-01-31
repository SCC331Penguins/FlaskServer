import json
from Database import dbhandler
from Authentication import authenticator
from WAMP import packet

def handlePacket(message):
    #token = payload.getToken(packet)
    #if authenticator.verify_token(token) == False:
        #return "Invalid token"
        #pass

    type = packet.getType(message)

    packet_payload = packet.getPayload(message)

    print(packet.Type.REGISTER)

    if type == packet.Type.INIT_ROUTER:
        pass
    elif type == packet.Type.LOGIN:
        print(login(packet_payload))
        pass
    elif type == packet.Type.REGISTER:
        print(register(packet_payload))
        pass
    elif type == packet.Type.REQUEST_ROUTERS:
        pass
    elif type == packet.Type.REQUEST_ROUTERS_SENSORS:
        pass
    elif type == packet.Type.UPDATE_SENSORS:
        pass
    elif type == packet.Type.UPDATE_WIFI:
        pass
    else:
        print("invalid type")
        return

def login(packet_payload):
    db = dbhandler.DbHandler()
    return db.login_user(packet_payload['username'], packet_payload['password'])

def register(packet_payload):
    db = dbhandler.DbHandler()
    return db.create_user(packet_payload['username'], packet_payload['password'])
