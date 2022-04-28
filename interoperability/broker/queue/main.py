from threading import Thread
from interoperability.broker.controller.controllerService import ControllerService
from ..handler.httpHandler import HTTPHandler
from ...persistence.persistence_provider import PersistenceProvider

def start():
    controllerService1 = ControllerService(1, None)
    controllerService2 = ControllerService(2, None)
    httpHandler1 = HTTPHandler(2700, controllerService1.request)
    httpHandler2 = HTTPHandler(2701, controllerService2.request)
    persistenceProvider = PersistenceProvider()