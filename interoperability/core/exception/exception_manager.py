import os, sys
class ExceptionManager():
    def __init__(self):
        self.__dir = f"{os.getcwd()}/logs"

    def handle_exception(self, exception):
        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)
        file_name = f"{self.__dir}/exception.log"
        with open(file_name, 'a') as file:
            file.write(f"{exception}\n")
        print(f"Exception has been logged to {file_name}")