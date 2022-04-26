from interoperability.broker.main import start
from threading import Thread

def main():
    start()
    input('Press enter to close broker')

if __name__ == "__main__":
    main()