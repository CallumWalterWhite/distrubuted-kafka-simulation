import socket
import json

## Sender class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class create socket connections to a remote server.
class Sender():
    ## __init__ method.
    #  @param self The object pointer.
    #  @param host The host to connect to.
    #  @param port The port to connect to.
    def __init__(self, address, port, buffer_size=128000, decoder='UTF-8'):
        self.address = address
        self.port = port
        self.buffer_size = buffer_size
        self.decoder = decoder

    ## send method.
    #  @param self The object pointer.
    #  @param message The message to send.
    #  @return The response from the server.
    #  @details This method will send a message to the server and return the response.
    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.address, self.port))
                json_data = message.toJSON().encode()
                s.sendall(json_data)
                data = s.recv(self.buffer_size)
                json_data = str(data.decode(self.decoder))
                response_object = json.loads(json_data)
                if response_object['status_code'] == 200:
                    return response_object['data']
                else:
                    raise Exception(response_object['error_message'])
    ## async send method.
    #  @param self The object pointer.
    #  @param message The message to send.
    #  @details This method will send a message to the server and return the response.
    async def send_async(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.address, self.port))
                json_data = message.toJSON().encode()
                s.sendall(json_data)
                data = s.recv(self.buffer_size)
                json_data = str(data.decode(self.decoder))
                response_object = json.loads(json_data)