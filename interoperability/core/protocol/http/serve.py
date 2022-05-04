from socketserver import TCPServer
from .handler import HttpRequestHandler
from threading import Thread
import asyncio

class HTTPServe():
    __port: int = 8080
    __alive_thread: Thread
    __reflection_class = None
    def __init__(self, port: int, reflection_class):
        self.__port = port
        self.__reflection_class = reflection_class
        self.__alive_thread = Thread(target=asyncio.run, args=(self.__create(),))
        self.__alive_thread.start()
    
    async def __create(self):
        with TCPServer(("", self.__port), HttpRequestHandler) as httpd:
            httpd.reflection_class = self.__reflection_class
            await httpd.serve_forever()