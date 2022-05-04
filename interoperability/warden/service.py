from uuid import uuid4
from interoperability.persistence.repository import Repository


class Service():
    __repo: Repository

    def __init__(self, repo: Repository):
        self.__repo = repo

    def add_broker(self, id, address, port):
        self.__repo.add_broker(id, address, port)
        print("broker added...")
        

    def list_brokers(self):
        return self.__repo.list_brokers()
        
        