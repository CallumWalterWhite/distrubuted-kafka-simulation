import json
import socket
import sys, os
sys.path.append(f"{os.getcwd()}/interoperability/core")
sys.path.append(f"{os.getcwd()}/interoperability")
from core import Message, ADD_MEESAGE

def main():
    print('test')
    test_pushing_message()
    pass

def test_pushing_message():
    topic_id = input()
    topic_message = input()
    address = '127.0.0.1'
    port = 2700
    BUFFER_SIZE=1024
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((address, port))
        message : Message = Message(ADD_MEESAGE, {
            "id": topic_id,
            "message": topic_message
        })
        json_data = message.toJSON().encode()
        print(json_data)
        s.sendall(json_data)
        data = s.recv(BUFFER_SIZE)
        json_data = str(data.decode("utf-8"))
        print(json_data)

if __name__ == '__main__':
    main()

