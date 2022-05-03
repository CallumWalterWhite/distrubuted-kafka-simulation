from interoperability.warden.commands import Command
from interoperability.warden.config import DEFAULT_PORT, DEFAULT_NAME
from interoperability.core.handler.http_handler import HTTPHandler
from interoperability.persistence.persistence_provider import PersistenceProvider
from interoperability.warden.service import Service

def start_warden():
    print('Welecome to warden, broker manager and register \n')
    print(f'Starting TCP socket on port {DEFAULT_PORT} \n')
    service = Service(DEFAULT_NAME, PersistenceProvider.getRepo(DEFAULT_NAME))
    HTTPHandler(DEFAULT_PORT, service)
    Command(service)