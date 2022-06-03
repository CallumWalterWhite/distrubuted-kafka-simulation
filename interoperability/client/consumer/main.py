import json
import socket
import sys, os
import time
sys.path.append(f"{os.getcwd()}/interoperability/core")
sys.path.append(f"{os.getcwd()}/interoperability")
from core import (Message, GET_CLUSTER_INFO, GET_MEESAGES)
from config import *

def main():
    consumer_group_name = input('Please enter consumer group name - ')
    cluster_info = get_cluster_info(consumer_group_name)
    index = 1
    for info in cluster_info:
        print(f'{index}. {info["topic"]}')
        index += 1
    selection = int(input("Please select a topic..."))
    topic_broker = cluster_info[selection - 1]
    while(True):
        get_messages(consumer_group_name, topic_broker['topic_id'], topic_broker['broker_address'], int(topic_broker['broker_port']))
        time.sleep(ITERATION_PULL)

def get_cluster_info(consumer_group_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((CLUSTER_ADDRESS, CLUSTER_WARDEN_PORT))
        message : Message = Message(GET_CLUSTER_INFO, {
            "consumer_group_name": consumer_group_name
        })
        json_data = message.toJSON().encode()
        s.sendall(json_data)
        data = s.recv(BUFFER_SIZE)
        return json.loads(str(data.decode("utf-8")))
    
def get_messages(consumer_group_name, topic_id, address, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((address, port))
        message : Message = Message(GET_MEESAGES, {
            "id": topic_id,
            "consumer_group_name": consumer_group_name
        })
        json_data = message.toJSON().encode()
        print(json_data)
        s.sendall(json_data)
        data = s.recv(BUFFER_SIZE)
        json_data = str(data.decode("utf-8"))
        print(json_data)

if __name__ == '__main__':
    main()