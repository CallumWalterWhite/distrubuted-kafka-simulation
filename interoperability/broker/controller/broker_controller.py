from uuid import uuid4, UUID
from service.broker_service import BrokerService
import json


class BrokerController():
    __service: BrokerService

    def __init__(self, service: BrokerService):
        self.__service = service

    def add_topic(self, body):
        data = json.loads(body[1:-1])
        name = data['name']
        id = uuid4()
        return self.__service.add_topic(name)

    def add_message(self, body):
        data = json.loads(body[1:-1])
        id = UUID(data['id'])
        message = data['message']
        return self.__service.add_message(id, message)
