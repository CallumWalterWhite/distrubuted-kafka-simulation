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
        
    def get_cluster_info(self, body):
        return self.__service.cluster_info(body['consumer_group_name'])
    
    def get_consumer_group_offset(self, body):
        return {
            "offset": self.__service.get_partition_offset_by_consumer_group(body['topic_id'], body['broker_id'], body['consumer_group_name'])
        }
    
    def set_consumer_group_offset(self, body):
        return {
            "offset": self.__service.set_partition_offset_by_consumer_group(body['topic_id'], body['broker_id'], body['consumer_group_name'], body['offset'])
        }