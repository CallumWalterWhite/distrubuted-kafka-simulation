import socket
import json

class Sender():
    def __init__(self, address, port, buffer_size=1024, decoder='UTF-8'):
        self.address = address
        self.port = port
        self.buffer_size = buffer_size
        self.decoder = decoder

    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.address, self.port))
                json_data = message.toJSON().encode()
                s.sendall(json_data)
                data = s.recv(self.buffer_size)
                json_data = str(data.decode(self.decoder))
                response_object = json.loads(json_data)
                return response_object
    
    async def send_async(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.address, self.port))
                json_data = message.toJSON().encode()
                s.sendall(json_data)
                data = s.recv(self.buffer_size)
                json_data = str(data.decode(self.decoder))
                response_object = json.loads(json_data)