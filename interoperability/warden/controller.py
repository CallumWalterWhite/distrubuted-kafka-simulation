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