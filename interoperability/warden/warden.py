
from uuid import uuid4
import array
from threading import Thread
import asyncio
from interoperability.warden.config import *
from interoperability.broker.broker import Broker
from interoperability.broker.controller.broker_controller import BrokerController
from interoperability.broker.service.broker_service import BrokerService
from interoperability.core.protocol.tcp.serve import TCPServe
from interoperability.warden.service import Service
from interoperability.client.consumer.consumer import Consumer
from warden.controller import Controller
from warden.persistence.repository import Repository

## Warden class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  @todo    Add replication for partitions.
#  
#  @details This class is used to create a warden.
#  The warden will manage the brokers, topics, and partitions.
class Warden():
    ## Service variable
    __service: Service
    ## TCP instance variable
    __tcp_serve: TCPServe

    ## __init__ method.
    #  @param self The object pointer.
    #  @return None
    #  @details Constructor for the Warden class.
    def __init__(self):
        service = Service(Repository())
        controller = Controller(service)
        tcp_serve = TCPServe(DEFAULT_PORT, controller)
        self.__service = service
        self.__tcp_serve = tcp_serve
        print('Welecome to warden, broker manager and register \n')
        print(f'Starting TCP socket on port {DEFAULT_PORT} \n')
        
        self.__print_menu()

    ## __print_menu method.
    #  @param self The object pointer.
    #  @details Prints the menu.
    def __print_menu(self):
        print('---------------------------------- ')
        print('1. Start Broker')
        print('2. List Brokers')
        print('3. Add topic')
        print('4. List topics')
        print('5. View messages in topic')
        print('6. List Consumers')
        print('7. Stop warden')
        print('---------------------------------- \n')
        user_selection = input()
        self.__command_factory(user_selection)

    ## __start_broker method:
    # @param self The object pointer.
    # @details Starts a broker and adds it to the service.
    def __start_broker(self):
        print('--------- Starting broker ---------')
        print('-----------------------------------')
        print('Broker starting \n')
        id = uuid4()
        broker = Broker(id)
        broker_service = BrokerService(broker)
        controller = BrokerController(broker_service)
        broker.assign_handler(controller)
        self.__service.add_broker(broker.id, BROKER_LOCAL_IP, broker.port)
        print('--------- Broker registerd -------- \n')
        print('-----------------------------------')
    
    ## __stop method
    #  @param self The object pointer.
    #  @details Stops the warden and deletes all brokers.
    def __stop(self):
        self.__service.delete_all_brokers()
        self.__tcp_serve.close()
    
    ## __add_topic method
    #  @param self The object pointer.
    #  @details Registers a topic and number of partitions and adds it to the service.
    def __add_topic(self):
        print('---------- Adding topic -----------')
        print('-----------------------------------')
        brokers = self.__service.list_brokers()
        if len(brokers) == 0:
            print('Broker list empty')
            return
        print('Please enter topic name... \n')
        topic_name = input()
        print('Please enter number of partitions... \n')
        number_of_partitions = self.__get_number_input()
        
        #TODO: Add replication for partitions.
        replication_factor = 0
    
        is_done = self.__service.add_topic(topic_name, number_of_partitions, replication_factor)
        if is_done:
            print(f'Topic added to brokers')
        else:
            print(f'Error adding topic to brokers')
        print('-----------------------------------')

    ## __list_brokers method
    #  @param self The object pointer.
    #  @details Lists all brokers.
    def __list_brokers(self):
        for row in self.__service.list_brokers():
            print(row)

    ## __list_consumes method
    #  @param self The object pointer.
    #  @details Lists all consumers.
    def __list_consumes(self):
        for consumer in self.__service.list_consumer_groups():
            print(f"{consumer[0]} - {consumer[1]}" + '\n')
    
    ## __list_topics method
    #  @param self The object pointer.
    #  @details Lists all topics.
    def __list_topics(self):
        topics = self.__service.list_topics()
        for topic in topics:
            print(f"{topic[0]} - {topic[1]}" + '\n')
    
    ## __view_topic_messages method
    #  @param self The object pointer.
    #  @details Lists all messages in a topic.
    def __view_topic_messages(self):
        topics = self.__service.list_topics()
        index = 1
        for info in topics:
            print(f'{index}. {info[1]}')
            index += 1
        selection = int(input("Please select a topic..."))
        topic = topics[selection - 1]
        cluster = self.__service.cluster_info()
        topic_brokers = list(filter(lambda x: x['topic_id'] == topic[0], cluster))
        messages = self.__service.get_topic_messages(topic_brokers)
        print(f'------- Messages in {topic[1]}  ------- ' + '\n')
        print(f'------- Warning!  ------- ' + '\n')
        print(f'------- Messages not in order  ------- ' + '\n')
        print(messages)
        print('-----------------------------------')

    ## __command_factory method
    #  @param self The object pointer.
    #  @param user_selection The user selection.
    #  @details Creates a command based on the user selection.
    def __command_factory(self, user_selection):
        if user_selection == '1':
            self.__start_broker()
            self.__print_menu()
        elif user_selection == '2':
            self.__list_brokers()
            self.__print_menu()
        elif user_selection == '3':
            self.__add_topic()
            self.__print_menu()
        elif user_selection == '4':
            self.__list_topics()
            self.__print_menu()
        elif user_selection == '5':
            self.__view_topic_messages()
            self.__print_menu()
        elif user_selection == '6':
            self.__list_consumes()
            self.__print_menu()
        elif user_selection == '7':
            self.__stop()
        else:
            print('Wrong input \n')
            self.__print_menu()

    ## __get_number_input method
    #  @param self The object pointer.
    #  @details Gets a number input from the user.
    def __get_number_input(self):
        user_input = input()
        try:
            return int(user_input)
        except ValueError:
            print('Wrong input \n')
            return self.__get_number_input()

