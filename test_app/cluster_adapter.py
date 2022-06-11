from core.protocol.model.message_type import *
from core.protocol.model.message import Message
from core.protocol.tcp.sender import Sender

class ClusterAdapter():
    def __init__(self):
        self.address = '127.0.0.1'
        self.port = 2500
    
    def get_cluster_info(self):
        cluster_info = None
        try:
            sender: Sender = Sender(self.address, self.port)
            response = sender.send(Message(GET_CLUSTER_INFO, {
                }))
            cluster_info = response
        except Exception as e:
            print(e)
        return cluster_info
    
    def check_cluster_status(self):
        try:
            sender: Sender = Sender('127.0.0.1', 2500)
            response = sender.send(Message(HEALTH_CHECK, {
                }))
            if response['status'] == 'ok':
                return True
        except Exception as e:
            return False
        return False