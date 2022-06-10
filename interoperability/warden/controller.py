from uuid import uuid4
from core.exception.exception_manager import ExceptionManager
from .service import Service

class Controller():
    __service: Service
    __exception_manager: ExceptionManager

    def __init__(self, service):
        self.__service = service
        self.__exception_manager = ExceptionManager()

    def register_broker(self, body):
        id = None
        try:
            id = uuid4()
            self.__service.add_broker(id, body['address'], body['port'])
        except Exception as e:
            self.__exception_manager.handle(e)
        return {
            "id": id
        }

    def add_consumer_group(self, body):
        id = None
        try:
            id = str(self.__service.add_consumer_group(body['consumer_group_name']))
        except Exception as e:
            self.__exception_manager.handle(e)
        return {
            "id": id
        }
        
    def get_cluster_info(self, body):
        cluster_info = None
        try:
            cluster_info = self.__service.cluster_info()
        except Exception as e:
            self.__exception_manager.handle(e)
        return cluster_info
    
    def health_check(self, body):
        return {
            "status": "ok"
        }
    
    def get_consumer_group_offset(self, body):
        return {
            "offset": self.__service.get_partition_offset_by_consumer_group(body['partition_id'], body['broker_id'], body['consumer_group_id'])
        }
    
    def set_consumer_group_offset(self, body):
        return {
            "offset": self.__service.set_partition_offset_by_consumer_group(body['partition_id'], body['broker_id'], body['consumer_group_id'], body['offset'])
        }