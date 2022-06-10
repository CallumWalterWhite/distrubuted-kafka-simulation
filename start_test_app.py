from test_app.test_app import TestApp

def main():
    try:
        TestApp()
    except Exception as ex:
        print('Caught this error: ' + repr(ex))
        print('Error has occured on test app, instance is stopping....')

if __name__ == "__main__":
    main()