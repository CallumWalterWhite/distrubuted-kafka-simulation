from socketserver import TCPServer

from interoperability.broker.controller.controller_service import ControllerService
from .request_handler import RequestHandler
from threading import Thread
import asyncio

class HTTPHandler():
    __port: int = 8080
    __alive_thread: Thread
    __reflection_class = None
    def __init__(self, port: int, reflection_class):
        self.__port = port
        self.__reflection_class = reflection_class
        self.__alive_thread = Thread(target=asyncio.run, args=(self.__create(),))
        self.__alive_thread.start()
    
    async def __create(self):
        with TCPServer(("", self.__port), RequestHandler) as httpd:
            httpd.reflection_class = self.__reflection_class
            await httpd.serve_forever()