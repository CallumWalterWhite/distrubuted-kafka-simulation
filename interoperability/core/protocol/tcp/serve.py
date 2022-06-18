from socketserver import TCPServer
from threading import Thread
import asyncio
from .handler import TcpRequestHandler

## TCPServe class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class creates a thread with a TCPServer socket connection.
class TCPServe():
    ## Port variable
    __port: int = 2700
    ## Thread with TCPServer socket connection variable
    __alive_thread: Thread
    ## class reference variable
    __class_ref = None
    ## TCPServer variable
    __httpd: TCPServer

    ## __init__ method.
    #  @param self The object pointer.
    #  @param port The port to connect to.
    #  @param class_ref The class reference to invoke the method on.
    def __init__(self, port: int, class_ref):
        self.__port = port
        self.__class_ref = class_ref
        self.__alive_thread = Thread(target=asyncio.run, args=(self.__create(),))
        self.__alive_thread.start()
    
    ## __create method.
    #  @param self The object pointer.
    #  @return The TCPServer object.
    #  @details This method creates the TCPServer object.
    async def __create(self):
        with TCPServer(("", self.__port), TcpRequestHandler) as self.__httpd:
            self.__httpd.class_ref = self.__class_ref
            try:
                await self.__httpd.serve_forever()
            except:
                #THROWS ON SHUTDOWN
                print('Server shutting down....')
                self.__httpd.shutdown()
    
    ## close method.
    #  @param self The object pointer.
    #  @details This method closes the TCPServer object.
    def close(self):
        self.__httpd.shutdown()