import os
## ExceptionManager class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is used to manage exceptions.
class ExceptionManager():
    ## __init__ method.
    #  @param self The object pointer.
    def __init__(self):
        # set the directory to log exceptions to
        self.__dir = f"{os.getcwd()}/logs"
    ## handle method.
    #  @param self The object pointer.
    #  @param exception The exception to handle.
    #  @details This method will handle the exception and log it to a file.
    def handle_exception(self, exception):
        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)
        file_name = f"{self.__dir}/exception.log"
        with open(file_name, 'a') as file:
            file.write(f"{exception}\n")
        print(f"Exception has been logged to {file_name}")