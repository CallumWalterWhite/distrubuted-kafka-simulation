import json
import socket
import sys, os
sys.path.append(f"{os.getcwd()}/interoperability/core")
sys.path.append(f"{os.getcwd()}/interoperability")
from core import Message, GET_MEESAGES

def main():
    print('test')
    test_get_messages()
    pass

def test_get_messages():
    topic_id = input()
    address = '127.0.0.1'
    port = 2700
    BUFFER_SIZE=1024
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((address, port))
        message : Message = Message(GET_MEESAGES, {
            "id": topic_id
        })
        json_data = message.toJSON().encode()
        print(json_data)
        s.sendall(json_data)
        data = s.recv(BUFFER_SIZE)
        json_data = str(data.decode("utf-8"))
        print(json_data)

if __name__ == '__main__':
    main()

