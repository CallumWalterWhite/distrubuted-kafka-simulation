from interoperability.core.protocol.tcp.serve import TCPServe
from interoperability.warden.commands import Command
from interoperability.warden.config import DEFAULT_NAME, DEFAULT_PORT
from interoperability.warden.controller import Controller
from interoperability.warden.service import Service
from interoperability.warden.persistence.repository import Repository

def start_warden():
    print('Welecome to warden, broker manager and register \n')
    print(f'Starting TCP socket on port {DEFAULT_PORT} \n')
    service = Service(Repository())
    controller = Controller(service)
    tcp_serve = TCPServe(DEFAULT_PORT, controller)
    Command(tcp_serve, service)