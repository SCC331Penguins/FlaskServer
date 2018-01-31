from enum import Enum

class Type(object):
    INIT_ROUTER = 1
    UPDATE_SENSORS = 2
    UPDATE_WIFI = 3
    LOGIN = 4
    REGISTER = 5
    REQUEST_ROUTERS = 6
    REQUEST_ROUTERS_SENSORS = 7

def createPacket(type, token, payload, source):
    return {"token": token, "type":type, "payload":payload, "source":source}

def getType(packet):
    return packet["type"]

def getToken(packet):
    return packet["token"]

def getPayload(packet):
    return packet["payload"]

def getSource(packet):
    return packet["source"]