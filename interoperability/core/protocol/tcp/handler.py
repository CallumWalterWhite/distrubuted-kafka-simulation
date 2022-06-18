import json
from exception.custom.service_exception import ServiceException
from ..model.message import Message
import socketserver
from uris.identifier import URIIdentifier

## TcpRequestHandler class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is the callback class reference for the TCPServe class to invoke when request is sent.
#  Inherits from socketserver.BaseRequestHandler.
class TcpRequestHandler(socketserver.BaseRequestHandler):
    ## buffer size variable
    __BUFFER_SIZE=128000
    # handle method
    # @param self The object pointer. 
    # @details This method is the callback method for the TCPServe class to invoke when request is sent.
    def handle(self):
        self.data = self.request.recv(self.__BUFFER_SIZE).strip()
        try:
            json_data = str(self.data.decode("utf-8"))
            message : Message = json.loads(json_data)
            uri_response = URIIdentifier.invoke_function(self.server.class_ref, message["message_type"], message["body"])
            json_response = json.dumps({
                "status_code": 200,
                "data": uri_response
            })
            self.request.sendall(json_response.encode())
        except ServiceException as ex:
            json_response = json.dumps({
                "status_code": 500,
                "error_message": ex.message
            })
            self.request.sendall(json_response.encode())
        except Exception as ex:
            json_response = json.dumps({
                "status_code": 500,
                "error_message": ""
            })
            self.request.sendall(json_response.encode())
