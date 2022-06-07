import json
import socket
import sys, os
import time
sys.path.append(f"{os.getcwd()}/interoperability/core")
sys.path.append(f"{os.getcwd()}/interoperability")
from core import (Message, GET_CLUSTER_INFO, ADD_MEESAGE)
from config import *

from config import *
from publisher import Publisher

def main():
    publisher: Publisher = Publisher()
    topics = publisher.get_topics()
    index = 1
    for info in topics:
        print(f'{index}. {info["topic"]}')
        index += 1
    selection = int(input("Please select a topic... \n"))
    topic_id = topics[selection - 1]["topic_id"]
    message=input("Please enter a message... \n")
    n = int(input("Please the amount of times you want the message to send... \n"))
    publisher.publish(topic_id, message, n)

if __name__ == '__main__':
    main()