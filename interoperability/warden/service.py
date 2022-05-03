from interoperability.persistence.repository import Repository


class Service():
    __id: str
    __repo: Repository

    def __init__(self, id, repo: Repository):
        self.__id = id
        self.__repo = repo

    def get_brokers(self, body):
        print('13')

    def register_broker(self, id, address, port):
        self.__repo.add_broker(id, address, port)