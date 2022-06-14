from uuid import uuid4, UUID
from core.exception.exception_manager import ExceptionManager
from service.broker_service import BrokerService

class BrokerController():
    __service: BrokerService
    __exception_manager: ExceptionManager

    def __init__(self, service: BrokerService):
        self.__service = service
        self.__exception_manager = ExceptionManager()

    def add_message(self, data):
        isDone = False
        try:
            topic_id = UUID(data['topic_id'])
            partition_id = UUID(data['partition_id'])
            message = data['message']
            isDone = self.__service.add_message(topic_id, partition_id, message)
        except Exception as e:
            self.__exception_manager.handle(e)
        return {
            "isDone": isDone
        }
        
    def get_messages(self, data):
        messages = []
        try:
            id = UUID(data['id'])
            consumer_group_id = UUID(data['consumer_group_id'])
            messages = self.__service.get_messages(id, consumer_group_id)
        except Exception as e:
            self.__exception_manager.handle(e)
        return {
            "messages": messages
        }

    def add_topic(self, data):
        isDone = False
        try:
            id = UUID(data['id'])
            name = data['name']
            isDone = self.__service.add_topic(id, name)
        except Exception as e:
            self.__exception_manager.handle(e)
        return {
            "isDone": isDone
        }
    
    def add_partition(self, data):
        isDone = False
        try:
            id = UUID(data['id'])
            topic_id = UUID(data['topic_id'])
            leader = bool(data['leader'])
            isDone = self.__service.add_partition(topic_id, id, leader)
        except Exception as e:
            self.__exception_manager.handle(e)
        return {
            "isDone": isDone
        }

    def get_all_messages(self, data):
        messages = []
        try:
            id = UUID(data['id'])
            messages = self.__service.get_all_messages(id)
        except Exception as e:
            self.__exception_manager.handle(e)
        return {
            "messages": messages
        }