import sys
from controller.controllerService import ControllerService
from ioc.controller.container import ControllerContainer
from ..core.handler.httpHandler import HTTPHandler
from interoperability.persistence.persistence_provider import PersistenceProvider
from interoperability.persistence.repository import Repository
from dependency_injector.wiring import Provide

def main(port: int,
        controller_service: ControllerService = Provide[ControllerContainer.controller],):
    HTTPHandler(port, controller_service.request)


if __name__ == "__main__":
    application = ControllerContainer()
    application.core.init_resources()
    application.wire(modules=[__name__])

    main(2700)