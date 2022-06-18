import asyncio
import sys, os
from threading import Thread
sys.path.append(f"{os.getcwd()}/interoperability/core")
sys.path.append(f"{os.getcwd()}/interoperability")
sys.path.append(f"{os.getcwd()}/interoperability/client/publisher")
from core import *
from config import *

## Publisher class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  @todo    Add replication for partitions.
#  
#  @details This class is used to create a Publisher.
#  The Publisher will publish messages to a broker with a topic. 
class Publisher():
    ## __init__ method.
    # @param self The object pointer.
    # @param address The address of the warden.
    # @param port The port of the warden.
    def __init__(self, address, port):
        self.__address = address
        self.__port = port
        # Get cluster info
        self.__cluster_info = self.__get_cluster_info()

    ## bootstrap_publisher method.
    # @details This method is used to bootstrap a publisher.
    def bootstrap_publisher():
        publisher: Publisher = Publisher(CLUSTER_ADDRESS, CLUSTER_WARDEN_PORT)
        while True:
            topics = publisher.get_topics()
            index = 1
            for info in topics:
                print(f'{index}. {info["topic"]}')
                index += 1
            selection = int(input("Please select a topic... \n"))
            topic_id = topics[selection - 1]["topic_id"]
            message=input("Please enter a message... \n")
            n = int(input("Please the number of times you want the message to send... \n"))
            publisher.publish(topic_id, message, n)
            print('Messages pushed to brokers... \n')
            print('Press any q to quit...')
            x = input()
            if x == 'q':
                break
    
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
    
    ## publish method.
    # @param self The object pointer.
    # @param topic_id The topic id.
    # @param topic_message The topic message.
    # @param n The number of times to publish the message.
    # @details This method is used to publish a message to a topic.
    def publish(self, topic_id, topic_message, n):
        cluster_info = self.__get_cluster_info()
        topic_brokers = [x for x in cluster_info if x["topic_id"] == topic_id]
        #TODO: implement weighted round robin by requesting partition sizes
        if len(topic_brokers) > n:
            pass
        else:
            # batch messages by broker and calulate the number of messages to send
            batch_size = n // len(topic_brokers)
            batch_size_r = n % len(topic_brokers)
            i = 0
            for topic_broker in topic_brokers:
                size_n = batch_size
                if i == (len(topic_brokers) - 1):
                    size_n = batch_size + batch_size_r
                i += 1
                messages = []
                for x in range(0, (size_n)):
                    messages.append(topic_message)
                Thread(target=asyncio.run, args=(self.__publish_message(topic_broker['topic_id'], topic_broker['partition_id'], topic_broker, messages),)).start()
    ## __add_message method.
    # @param self The object pointer.
    # @param topic_id The topic id.
    # @param partition_id The partition id.
    # @param broker The broker.
    # @param topic_message The topic message.
    # @details This method is used to send a message to a broker with a topic and partition.
    async def __publish_message(self, topic_id, partition_id, broker, topic_messages):
        try:
            sender: Sender = Sender(broker['broker_address'], int(broker['broker_port']), BUFFER_SIZE)
            response = await sender.send_async( Message(ADD_MEESAGE, {
                "topic_id": topic_id,
                "partition_id": partition_id,
                "messages": topic_messages
            }))
            return response
        except Exception as e:
            print(e)