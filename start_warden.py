from interoperability.warden.main import start_warden

def main():
    try:
        start_warden()
    except Exception:
        print('Error has occured on warden thread, instance is stopping....')

if __name__ == "__main__":
    main()