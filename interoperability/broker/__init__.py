import os, sys
sys.path.append(f"{os.getcwd()}/interoperability/broker")
sys.path.append(f"{os.getcwd()}/interoperability/core")
sys.path.append(f"{os.getcwd()}/interoperability")
from broker import Broker
from service.broker_service import BrokerService
from controller.broker_controller import BrokerController

def main(composite=True):    
    if composite:
        broker = Broker()
        service = BrokerService(broker)
        controller = BrokerController(service)
        broker.assign_handler(controller)
        input("Press any key to close broker...")
        broker.close()
        

if __name__ == '__main__':
    main()