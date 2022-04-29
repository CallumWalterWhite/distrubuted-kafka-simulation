from uuid import UUID, uuid4
from interoperability.broker.controller.controller_service import ControllerService
from interoperability.broker.registry.port_factory import PortFactory
from interoperability.core.handler.http_handler import HTTPHandler
from interoperability.persistence.persistence_provider import PersistenceProvider

class Broker():
    __id: UUID
    __port: int
    __controller_service: ControllerService
    __httpHandler: HTTPHandler
    def __init__(self):
        self.__port = PortFactory.get_first_available_port()
        self.__id = uuid4()
        self.__controller_service = ControllerService(self.__id, PersistenceProvider.getRepo(self.__id))
        self.__httpHandler = HTTPHandler(self.__port, self.__controller_service)