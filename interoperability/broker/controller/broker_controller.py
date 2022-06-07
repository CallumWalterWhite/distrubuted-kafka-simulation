from uuid import uuid4, UUID
from service.broker_service import BrokerService
import json


class BrokerController():
    __service: BrokerService

    def __init__(self, service: BrokerService):
        self.__service = service

    def add_message(self, data):
        topic_id = UUID(data['topic_id'])
        partition_id = UUID(data['partition_id'])
        message = data['message']
        return {
            'isDone': self.__service.add_message(topic_id, partition_id, message)
        }
        
    def get_messages(self, data):
        id = UUID(data['id'])
        consumer_group_id = UUID(data['consumer_group_id'])
        return {
            'messages': self.__service.get_messages(id, consumer_group_id)
        }

    def add_topic(self, data):
        id = UUID(data['id'])
        name = data['name']
        return {
            'isDone': self.__service.add_topic(id, name)
        }
    
    def add_partition(self, data):
        id = UUID(data['id'])
        topic_id = UUID(data['topic_id'])
        leader = bool(data['leader'])
        return {
            'isDone': self.__service.add_partition(topic_id, id, leader)
        }