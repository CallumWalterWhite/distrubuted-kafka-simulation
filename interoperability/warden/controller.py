from uuid import uuid4
from core.exception.exception_manager import ExceptionManager
from .service import Service

## Controller class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is used to create a controller object for the warden.
#  This is the entry point of the tcp server requests.
class Controller():
    # service variable
    __service: Service
    # exception_manager variable
    __exception_manager: ExceptionManager

    ## __init__ method.
    # @param self The object pointer.
    # @param service The service object.
    def __init__(self, service):
        self.__service = service
        self.__exception_manager = ExceptionManager()

    ## register_broker method.
    # @param self The object pointer.
    # @param body The body of the request.
    # @return id The id of the broker.
    def register_broker(self, body):
        id = None
        try:
            id = str(uuid4())
            self.__service.add_broker(id, body['address'], body['port'])
        except Exception as e:
            self.__exception_manager.handle(e)
        return {
            "id": id
        }

    ## add_consumer_group method.
    # @param self The object pointer.
    # @param body The body of the request.
    # @return id The id of the consumer group.
    def add_consumer_group(self, body):
        id = None
        try:
            id = str(self.__service.add_consumer_group(body['consumer_group_name']))
        except Exception as e:
            self.__exception_manager.handle(e)
        return {
            "id": id
        }
        
    ## get_cluster_info method.
    # @param self The object pointer.
    # @param body The body of the request.
    # @return cluster_info The cluster info.
    def get_cluster_info(self, body):
        cluster_info = None
        try:
            cluster_info = self.__service.cluster_info()
        except Exception as e:
            self.__exception_manager.handle(e)
        return cluster_info
    
    ## health_check method.
    # @param self The object pointer.
    # @param body The body of the request.
    # @return status The status of the health check.
    def health_check(self, body):
        return {
            "status": "ok"
        }
    
    ## get_consumer_group_offset method.
    # @param self The object pointer.
    # @param body The body of the request.
    # @return offset The offset of the partition.
    def get_consumer_group_offset(self, body):
        return {
            "offset": self.__service.get_partition_offset_by_consumer_group(body['partition_id'], body['broker_id'], body['consumer_group_id'])
        }
    
    ## set_consumer_group_offset method.
    # @param self The object pointer.
    # @param body The body of the request.
    # @return offset The offset of the partition.
    def set_consumer_group_offset(self, body):
        return {
            "offset": self.__service.set_partition_offset_by_consumer_group(body['partition_id'], body['broker_id'], body['consumer_group_id'], body['offset'])
        }