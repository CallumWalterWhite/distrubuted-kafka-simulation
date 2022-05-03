from http.client import UnknownProtocol


class URIIdentifier():
    def invoke_function(cref, fref: str, body):
        if (fref in [method_name for method_name in dir(type(cref))
                  if callable(getattr(type(cref), method_name))]) and '__' not in fref:
                    return getattr(type(cref), fref)(cref, body)
        else:
            raise UnknownProtocol('')