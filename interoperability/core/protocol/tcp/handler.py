from email.policy import default
from http.client import UnknownProtocol
import json
from ..model.message import Message
import socketserver
from core.uris.identifier import URIIdentifier

class TcpRequestHandler(socketserver.BaseRequestHandler):
    __BUFFER_SIZE=1024
    def handle(self):
        self.data = self.request.recv(self.__BUFFER_SIZE).strip()
        try:
            json_data = str(self.data.decode("utf-8"))
            message : Message = json.loads(json_data)
            uri_response = URIIdentifier.invoke_function(self.server.reflection_class, message["message_type"], message["body"])
            json_response = json.dumps(uri_response)
            self.request.sendall(json_response.encode())
        except Exception as ex:
            print(ex)
            self.request.sendall(b'500')
