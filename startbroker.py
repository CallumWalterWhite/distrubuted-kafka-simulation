from interoperability.broker.controller.main import start


def main():
    start(2700, '35DKTG-094F')
    start(2701, 'WDI54T-094F')
    input('Press enter to close broker \n ')

if __name__ == "__main__":
    main()