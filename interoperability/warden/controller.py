from uuid import uuid4
from .service import Service

class Controller():
    __service: Service

    def __init__(self, service):
        self.__service = service

    def register_broker(self, body):
        id = uuid4()
        self.__service.add_broker(id, body['address'], body['port'])
        return {
            "id": str(id)
        }

    
    def add_consumer_group(self, body):
        return {
            "id": str(self.__service.add_consumer_group(body['consumer_group_name']))
        }
        
    def get_cluster_info(self, body):
        return self.__service.cluster_info()
    
    def get_consumer_group_offset(self, body):
        return {
            "offset": self.__service.get_partition_offset_by_consumer_group(body['partition_id'], body['broker_id'], body['consumer_group_id'])
        }
    
    def set_consumer_group_offset(self, body):
        return {
            "offset": self.__service.set_partition_offset_by_consumer_group(body['partition_id'], body['broker_id'], body['consumer_group_id'], body['offset'])
        }