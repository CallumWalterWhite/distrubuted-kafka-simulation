from http.client import UnknownProtocol

## URIIdentifier class.
#  @author  Callum White
#  @version 1.0
#  @date    01/06/2022
#  @bug     No known bugs.
#  
#  @details This class is used to invoke methods on a object instance of the class with the method given.
class URIIdentifier():
    #invoke_function method.
    # @param class_ref The class reference to invoke the method on.
    # @param method_name The name of the method to invoke.
    # @param method_args The arguments to pass to the method.
    # @return The result of the method.
    # @details This method is used to invoke a method on a object instance of the class with the method given.
    def invoke_function(class_ref, method, body):
        if (method in [method_name for method_name in dir(type(class_ref))
                  if callable(getattr(type(class_ref), method_name))]) and '__' not in method:
                    return getattr(type(class_ref), method)(class_ref, body)
        else:
            raise UnknownProtocol('')