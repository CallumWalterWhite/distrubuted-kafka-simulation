import asyncio
import sys, os
from threading import Thread
import time
sys.path.append(f"{os.getcwd()}/interoperability/core")
sys.path.append(f"{os.getcwd()}/interoperability")
from core import *
from config import *

class Publisher():
    def __init__(self):
        self.__cluster_info = self.__get_cluster_info()
    
    def __get_cluster_info(self):
        sender: Sender = Sender(CLUSTER_ADDRESS, CLUSTER_WARDEN_PORT, BUFFER_SIZE)
        return sender.send(Message(GET_CLUSTER_INFO, {}))

    def get_topics(self):
        topics = [x["topic_id"] for x in self.__cluster_info]
        unique_topics = []
        for topic in list(set(topics)):
            unique_topics.append([x for x in self.__cluster_info if x["topic_id"] == topic][0])
        return unique_topics
    
    def publish(self, topic_id, topic_message, n):
        cluster_info = self.__get_cluster_info()
        topic_brokers = [x for x in cluster_info if x["topic_id"] == topic_id]
        #TODO: implement weighted round robin by requesting partition sizes
        if len(topic_brokers) > n:
            pass
        else:
            batch_size = n // len(topic_brokers)
            batch_size_r = n % len(topic_brokers)
            i = 0
            for topic_broker in topic_brokers:
                size_n = batch_size
                if i == (len(topic_brokers) - 1):
                    size_n = batch_size + batch_size_r
                i += 1
                print(size_n)
                for x in range(0, size_n):
                    Thread(target=asyncio.run, args=(self.__add_message(topic_broker['topic_id'], topic_broker['partition_id'], topic_broker, topic_message),)).start()

    async def __add_message(self, topic_id, partition_id, broker, topic_message):
        sender: Sender = Sender(broker['broker_address'], int(broker['broker_port']), BUFFER_SIZE)
        response = await sender.send_async( Message(ADD_MEESAGE, {
            "topic_id": topic_id,
            "partition_id": partition_id,
            "message": topic_message
        }))
        return response