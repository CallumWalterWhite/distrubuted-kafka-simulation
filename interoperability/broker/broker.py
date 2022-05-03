import array
from ctypes import Array
from inspect import stack
from uuid import UUID, uuid4
from interoperability.broker.registry.port_factory import PortFactory
from interoperability.broker.topic.topic import Topic
from interoperability.core.handler.http_handler import HTTPHandler

class Broker():
    topics: array
    id: UUID
    port: int
    __httpHandler: HTTPHandler
    def __init__(self, id):
        self.id = id
        self.topics = []

    def assign_handler(self, controller_service):
        self.port = PortFactory.get_first_available_port()
        self.__httpHandler = HTTPHandler(self.port, controller_service)

    def add_topic(self, topic: Topic):
        self.topics.append(topic)

    def get_topic(self, id):
        return [x for x in self.topics if x.id == id][0]