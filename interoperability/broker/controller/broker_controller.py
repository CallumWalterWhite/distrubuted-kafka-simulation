from uuid import uuid4, UUID
from core.exception.exception_manager import ExceptionManager
from service.broker_service import BrokerService

## BrokerController class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is used to create a controller object for the broker.
#  This is the entry point of the tcp server requests.
class BrokerController():
    __service: BrokerService
    __exception_manager: ExceptionManager

    ## __init__ method.
    # @param self The object pointer.
    # @param service The service object.
    def __init__(self, service: BrokerService):
        self.__service = service
        self.__exception_manager = ExceptionManager()

    ## add_message method.
    # @param self The object pointer.
    # @param body The body of the request.
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
        
    ## get_messages method.
    # @param self The object pointer.
    # @param body The body of the request.
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

    ## add_topic method.
    # @param self The object pointer.
    # @param body The body of the request.
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
    
    ## add_partition method.
    # @param self The object pointer.
    # @param body The body of the request.
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

    ## get_all_messages method.
    # @param self The object pointer.
    # @param body The body of the request.
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