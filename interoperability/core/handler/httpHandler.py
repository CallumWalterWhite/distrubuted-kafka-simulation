from socketserver import TCPServer

from interoperability.broker.controller.controllerService import ControllerService
from .requestHandler import RequestHandler
from threading import Thread
import asyncio

class HTTPHandler():
    __port: int = 8080
    __aliveThread: Thread
    __serviceCallback = None
    def __init__(self, port: int, serviceCallback):
        self.__port = port
        self.__serviceCallback = serviceCallback
        self.__aliveThread = Thread(target=asyncio.run, args=(self.__create(),))
        self.__aliveThread.start()
    
    async def __create(self):
        with TCPServer(("", self.__port), RequestHandler) as httpd:
            httpd.callback = self.__serviceCallback
            await httpd.serve_forever()