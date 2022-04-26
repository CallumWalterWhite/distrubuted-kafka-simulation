from socketserver import TCPServer

from interoperability.broker.controller.controllerService import ControllerService
from .httpRequestHandler import HTTPRequestHandler
from .protocolHandler import ProtocolHandler
from threading import Thread
import asyncio

class HTTPHandler(ProtocolHandler):
    __port: int = 8080
    __aliveThread: Thread
    def __init__(self, port: int):
        self.__port = port
        self.__aliveThread = Thread(target=asyncio.run, args=(self.__create(),))
        self.__aliveThread.start()
    
    async def __create(self):
        with TCPServer(("", self.__port), HTTPRequestHandler) as httpd:
            await httpd.serve_forever()