import array, sys, os
from uuid import UUID
from registry.warden_register import WardenRegister
from registry.port_factory import PortFactory
from topic.topic import Topic
from core import TCPServe

class Broker():
    topics: array
    id: UUID
    port: int
    __tcpServe: TCPServe
    def __init__(self, id=None):
        self.port = PortFactory.get_first_available_port()
        if id is None:
            id = WardenRegister.register(self.port)
        self.id = id
        self.topics = []

    def close(self):
        self.__tcpServe.close()

    def assign_handler(self, controller):
        self.__tcpServe = TCPServe(self.port, controller)

    def add_topic(self, topic: Topic):
        self.topics.append(topic)

    def get_topic(self, id):
        return [x for x in self.topics if x.id == id][0]