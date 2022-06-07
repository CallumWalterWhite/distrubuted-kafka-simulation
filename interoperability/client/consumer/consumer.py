import sys, os
import asyncio
sys.path.append(f"{os.getcwd()}/interoperability/core")
sys.path.append(f"{os.getcwd()}/interoperability/client/consumer")
from core import *
from config import *

class Consumer():
    def __init__(self, address, port, consumer_group_name):
        self.__address = address
        self.__port = port
        self.__consumer_group_name = consumer_group_name
        self.__consumer_group_id = self.__add_consumer_group()
        self.__cluster_info = self.__get_cluster_info()
    
    def __add_consumer_group(self):
        sender: Sender = Sender(self.__address, self.__port, BUFFER_SIZE)
        response = sender.send(Message(ADD_CONSUMER_GROUP, {
                "consumer_group_name": self.__consumer_group_name
            }))
        return response["id"]

    def __get_cluster_info(self):
        sender: Sender = Sender(self.__address, self.__port, BUFFER_SIZE)
        return sender.send(Message(GET_CLUSTER_INFO, {}))

    def get_topics(self):
        topics = [x["topic_id"] for x in self.__cluster_info]
        unique_topics = []
        for topic in list(set(topics)):
            unique_topics.append([x for x in self.__cluster_info if x["topic_id"] == topic][0])
        return unique_topics

    async def listen_to_cluster(self, topic_id):
        topic_brokers = [x for x in self.__cluster_info if x["topic_id"] == topic_id]
        while(True):
            for topic_broker in topic_brokers:
                sender: Sender = Sender(topic_broker['broker_address'], int(topic_broker['broker_port']), BUFFER_SIZE)
                response = sender.send(Message(GET_MEESAGES, {
                    "id": topic_id,
                    "consumer_group_id": self.__consumer_group_id
                }))
                if (len(response['messages']) > 0):
                    print(self.__consumer_group_name)
                    print(len(response['messages']))
            await asyncio.sleep(1)