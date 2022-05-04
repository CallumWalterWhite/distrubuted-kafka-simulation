import os, sys
sys.path.append(f"{os.getcwd()}/interoperability/broker")
from broker import Broker

def main(composite=True):    
    if composite:
        Broker()

if __name__ == '__init__':
    main()