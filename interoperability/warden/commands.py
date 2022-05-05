from uuid import uuid4
from interoperability.broker import Broker
from interoperability.broker.controller.broker_controller import BrokerController
from interoperability.broker.service.broker_service import BrokerService
from interoperability.core.protocol.tcp.serve import TCPServe
from interoperability.persistence.persistence_provider import PersistenceProvider
from interoperability.warden.service import Service


class Command():
    __service: Service
    __tcp_serve: TCPServe
    def __init__(self, tcp_serve: TCPServe, service: Service):
        self.__service = service
        self.__tcp_serve = tcp_serve
        self.__print_menu()

    def __print_menu(self):
        print('---------------------------------- ')
        print('1. Start Broker')
        print('2. List Brokers')
        print('3. Add topic')
        print('4. Stop warden')
        print('---------------------------------- \n')
        user_selection = input()
        self.__command_factory(user_selection)

    def __start_broker(self):
        print('Broker starting \n')
        id = uuid4()
        broker = Broker(id)
        broker_service = BrokerService(PersistenceProvider.getRepo(id), broker)
        controller = BrokerController(broker_service)
        broker.assign_handler(controller)
        self.__service.add_broker(broker.id, '127.0.0.1', broker.port)
        print('Broker registerd \n')

    def __stop(self):
        self.__service.delete_all_brokers()
        self.__tcp_serve.close()

    def __add_topic(self):
        brokers = self.__service.list_brokers()
        if len(brokers) == 0:
            print('Broker list empty')
            return
        i = 0
        for row in brokers:
            list_index = i + 1
            address = row[1]
            port = row[2]
            print(f'{list_index}. {address}:{port}')
            i = i + 1
        selection = int(input("Please choose a broker to add topic..."))
        broker = brokers[selection - 1]
        if broker is None:
            print('You do not enter a valid number')
            return
        topic_name = input("Please enter topic name...")
        is_done = self.__service.add_broker_topic(broker, topic_name)
        if is_done:
            print(f'Topic added to broker {broker[0]}')
        else:
            print(f'Error addoing topic to broker {broker[0]}')

    def __list_brokers(self):
        for row in self.__service.list_brokers():
            print(row)

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
            self.__stop()
        else:
            print('Wrong input \n')
            self.__print_menu()


