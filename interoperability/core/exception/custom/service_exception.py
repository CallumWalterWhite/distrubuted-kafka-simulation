## ServiceException
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#
#  @details This class is used to create a service exception.
class ServiceException(Exception):
    def __init__(self, message):
        self.message = message