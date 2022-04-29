from ...persistence.repository import Repository

class ControllerService():
    __id: str
    __repo: Repository

    def __init__(self, id, repo: Repository):
        self.__id = id
        self.__repo = repo

    def request(self, body):
        print(f"{self.__id} \n {body}")
    
    def get_brokers(self, body):
        print("test")