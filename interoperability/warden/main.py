import sys, os

from interoperability.warden.controller import Controller
from interoperability.warden.commands import Command
from interoperability.warden.config import DEFAULT_PORT, DEFAULT_NAME
from interoperability.core import TCPServe
from interoperability.persistence.persistence_provider import PersistenceProvider
from interoperability.warden.service import Service

def start_warden():
    print('Welecome to warden, broker manager and register \n')
    print(f'Starting TCP socket on port {DEFAULT_PORT} \n')
    service = Service(PersistenceProvider.getRepo(DEFAULT_NAME))
    controller = Controller(service)
    tcp_serve = TCPServe(DEFAULT_PORT, controller)
    Command(tcp_serve, service)