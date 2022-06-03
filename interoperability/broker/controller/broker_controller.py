from uuid import uuid4, UUID
from service.broker_service import BrokerService
import json


class BrokerController():
    __service: BrokerService

    def __init__(self, service: BrokerService):
        self.__service = service

    def add_message(self, data):
        id = UUID(data['id'])
        message = data['message']
        return self.__service.add_message(id, message)
        
    def get_messages(self, data):
        id = UUID(data['id'])
        consumer_group_name = data['consumer_group_name']
        return self.__service.get_messages(id, consumer_group_name)

    def add_topic(self, data):
        id = UUID(data['id'])
        name = data['name']
        self.__service.add_topic(id, name)
        return {
            'isDone': True
        }