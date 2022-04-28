from threading import Thread
from interoperability.broker.controller.controllerService import ControllerService
from interoperability.persistence.repository import Repository
from ..handler.httpHandler import HTTPHandler
from ...persistence.persistence_provider import PersistenceProvider

def start(port, id):
    repository: Repository = PersistenceProvider.getRepo(id)
    controllerService = ControllerService(id, repository)
    httpHandler = HTTPHandler(port, controllerService.request)
    