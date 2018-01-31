from .connection import *
import config
from Handlers import message_handler

class WAMP:

    def __init__(self):
        self.connections = [];
        self.connection = Connection('local',handler=self.handleMessage)
        self.connection.connect();

    def run(self):
        pass

    def handleMessage(self, channel, conName, message):
        message_handler.handlePacket(message)
        pass
