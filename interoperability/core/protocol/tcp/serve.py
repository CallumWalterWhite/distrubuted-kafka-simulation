from socketserver import TCPServer
from threading import Thread
import asyncio
from .handler import TcpRequestHandler

class TCPServe():
    __port: int = 2700
    __alive_thread: Thread
    __reflection_class = None
    __httpd: TCPServer
    def __init__(self, port: int, reflection_class):
        self.__port = port
        self.__reflection_class = reflection_class
        self.__alive_thread = Thread(target=asyncio.run, args=(self.__create(),))
        self.__alive_thread.start()
    
    async def __create(self):
        with TCPServer(("", self.__port), TcpRequestHandler) as self.__httpd:
            self.__httpd.reflection_class = self.__reflection_class
            try:
                await self.__httpd.serve_forever()
            except:
                #THROWS ON SHUTDOWN
                print('Server shutting down....')

    def close(self):
        self.__httpd.shutdown()