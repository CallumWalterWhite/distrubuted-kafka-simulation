import sys, os
import asyncio
from threading import Thread
sys.path.append(f"{os.getcwd()}/interoperability")
sys.path.append(f"{os.getcwd()}/interoperability/core")
sys.path.append(f"{os.getcwd()}/interoperability/client/consumer")
from core import *
from config import *

## Consumer class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  @todo    Add replication for partitions.
#  
#  @details This class is used to create a Consumer.
#  The Consumer will consume messages from a broker with a topic.
class Consumer():
    ## __init__ method.
    # @param self The object pointer.
    # @param address The address of the warden.
    # @param port The port of the warden.
    # @paramc consumer_group_name The name of the consumer group.
    def __init__(self, address, port, consumer_group_name):
        self.__address = address
        self.__port = port
        self.__consumer_group_name = consumer_group_name
        self.__consumer_group_id = self.__add_consumer_group()
        # Get cluster info
        self.__cluster_info = self.__get_cluster_info()
        self.__stop = False

    ## bootstrap_consumer method.
    # @details This method is used to bootstrap a consumer.
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
        #create a thread to consume messages per topic
        consumer_thread = Thread(target=asyncio.run, args=(consumer.subscribe(topic_ids),))
        consumer_thread.start()
        return consumer

    ## stop method.
    # @details This method is used to stop the consumer.
    def stop(self):
        self.__stop = True
    
    ## get_consumer_group_name method.
    # @details This method is used to get the consumer group name.
    def get_consumer_group_name(self):
        return self.__consumer_group_name
    
    ## get_consumer_group_id method.
    # @details This method is used to get the consumer id.
    def get_consumer_group_id(self):
        return self.__consumer_group_id

    ## __add_consumer_group method.
    # @details This method is used to add a consumer group.
    def __add_consumer_group(self):
        sender: Sender = Sender(self.__address, self.__port, BUFFER_SIZE)
        response = sender.send(Message(ADD_CONSUMER_GROUP, {
                "consumer_group_name": self.__consumer_group_name
            }))
        return response["id"]

    ## __get_cluster_info method.
    # @details This method is used to get the cluster info.
    def __get_cluster_info(self):
        sender: Sender = Sender(self.__address, self.__port, BUFFER_SIZE)
        return sender.send(Message(GET_CLUSTER_INFO, {}))

    ## get_topics method.
    # @details This method is used to get the topics.
    def get_topics(self):
        topics = [x["topic_id"] for x in self.__cluster_info]
        unique_topics = []
        for topic in list(set(topics)):
            unique_topics.append([x for x in self.__cluster_info if x["topic_id"] == topic][0])
        return unique_topics

    ## subscribe method.
    # @param self The object pointer.
    # @param topic_ids The topic ids.
    # @param callback The callback function.
    # @details This method is used to subscribe to a topic.
    async def subscribe(self, topic_ids, callback=None):
        topic_brokers = [x for x in self.__cluster_info if x["topic_id"] in topic_ids]
        # while loop to keep consuming messages
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
                        if (callback is not None):
                            callback(response['messages'])
                except Exception as e:
                    pass
            # sleep for a second before pulling messages again
            await asyncio.sleep(0.5)