import array, sys, os
from uuid import UUID
from registry.warden_register import WardenRegister
from registry.port_factory import PortFactory
from topic.topic import Topic
sys.path.append(f"{os.getcwd()}\interoperability")
from core import HTTPHandler

class Broker():
    topics: array
    id: UUID
    port: int
    __httpHandler: HTTPHandler
    def __init__(self, id=None):
        if id is None:
            id = WardenRegister.register()
        self.id = id
        self.topics = []

    def assign_handler(self, controller_service):
        self.port = PortFactory.get_first_available_port()
        self.__httpHandler = HTTPHandler(self.port, controller_service)

    def add_topic(self, topic: Topic):
        self.topics.append(topic)

    def get_topic(self, id):
        return [x for x in self.topics if x.id == id][0]