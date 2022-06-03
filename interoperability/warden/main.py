from interoperability.core.protocol.tcp.serve import TCPServe
from interoperability.persistence.persistence_provider import PersistenceProvider
from interoperability.warden.commands import Command
from interoperability.warden.config import DEFAULT_NAME, DEFAULT_PORT
from interoperability.warden.controller import Controller
from interoperability.warden.service import Service
from interoperability.warden.offset.offset_repository import OffsetRepository

def start_warden():
    print('Welecome to warden, broker manager and register \n')
    print(f'Starting TCP socket on port {DEFAULT_PORT} \n')
    service = Service(PersistenceProvider.getRepo(DEFAULT_NAME), OffsetRepository())
    controller = Controller(service)
    tcp_serve = TCPServe(DEFAULT_PORT, controller)
    Command(tcp_serve, service)