from email.policy import default
from uuid import uuid4
from interoperability.broker import Broker
from interoperability.broker.controller.controller_service import ControllerService
from interoperability.persistence.persistence_provider import PersistenceProvider
from interoperability.warden.service import Service


class Command():
    __service: Service
    __command_index = 0
    def __init__(self, service: Service):
        self.__service = service
        self.__command_index = 0
        self.__print_menu()

    def __print_menu(self):
        print('---------------------------------- ')
        print('1. Start Broker')
        print('2. List Brokers')
        print('3. Stop warden')
        print('---------------------------------- \n')
        user_selection = input()
        self.__command_factory(user_selection)

    def __start_broker(self):
        print('Broker starting \n')
        id = uuid4()
        broker = Broker(id)
        controller_service = ControllerService(id, PersistenceProvider.getRepo(id), broker)
        broker.assign_handler(controller_service)
        self.__service.register_broker(broker.id, 'localhost', broker.port)
        print('Broker registerd \n')

    def __stop(self):
        print('stopping....')

    def __list_brokers(self):
        pass

    def __command_factory(self, user_selection):
        if user_selection == '1':
            self.__start_broker()
            self.__print_menu()
        elif user_selection == '2':
            self.__list_brokers()
            self.__print_menu()
        elif user_selection == '3':
            self.__stop()
        else:
            print('Wrong input \n')
            self.__print_menu()


