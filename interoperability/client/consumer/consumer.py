import sys, os
import asyncio
from threading import Thread
sys.path.append(f"{os.getcwd()}/interoperability")
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
        self.__stop = False

    def bootstrap_consumer():
        consumer_group_name = input('Please enter consumer group name - ')
        consumer = Consumer(CLUSTER_ADDRESS, CLUSTER_WARDEN_PORT, consumer_group_name)
        topics = consumer.get_topics()
        topic_ids = []
        while(True):
            print('\n')
            index = 1
            topics_show = list(filter(lambda x: x['topic_id'] not in topic_ids, topics))
            for topic in topics_show:
                if (topic["topic_id"] not in topic_ids):
                    print(f'{index} - {topic["topic"]}')
                    index += 1
            if len(topic_ids) > 0:
                print('0 - Stop selection')
            print('\n')
            try:
                topic_index = int(input('Please enter topic index - '))
                if ((topic_index - 1) >= len(topics_show) or topic_index < 0):
                    raise Exception('Invalid topic index')
                if (topic_index == 0):
                    break
                topic_ids.append(topics_show[(topic_index - 1)]['topic_id'])
                if len(topic_ids) == len(topics):
                    break
            except Exception as e:
                print(e)
                continue
        consumer_thread = Thread(target=asyncio.run, args=(consumer.listen_to_cluster(topic_ids),))
        consumer_thread.start()
        return consumer

    def stop(self):
        self.__stop = True
    
    def get_consumer_group_name(self):
        return self.__consumer_group_name
    
    def get_consumer_group_id(self):
        return self.__consumer_group_id

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

    async def listen_to_cluster(self, topic_ids):
        topic_brokers = [x for x in self.__cluster_info if x["topic_id"] in topic_ids]
        while(self.__stop is not True):
            for topic_broker in topic_brokers:
                try:
                    sender: Sender = Sender(topic_broker['broker_address'], int(topic_broker['broker_port']), BUFFER_SIZE)
                    response = sender.send(Message(GET_MEESAGES, {
                        "id": topic_broker["topic_id"],
                        "consumer_group_id": self.__consumer_group_id
                    }))
                    if (len(response['messages']) > 0):
                        print(f"Messages pulled from topic - {topic_broker['topic']}")
                        print(f"Consumer group - {self.__consumer_group_name}")
                        print(f"Message Count - {len(response['messages'])}")
                        print(f"Messages - {response['messages']}")
                except Exception as e:
                    pass
            await asyncio.sleep(1)