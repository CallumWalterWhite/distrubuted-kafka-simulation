from http.client import UnknownProtocol
import json
import os
from http.server import BaseHTTPRequestHandler
from interoperability.core.uris.identifier import URIIdentifier

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = os.fspath(directory)
        super().__init__(*args, **kwargs)
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode("utf-8")
        (uri_request, parameter) = self.parse_request(self.data)
        try:
            uri_response = URIIdentifier.invoke_function(self.server.reflection_class, uri_request, parameter)
            json_response = json.dumps(uri_response)
            response = f'HTTP/1.1 200 OK\n\n{json_response}'
            self.request.sendall(response.encode())
        except UnknownProtocol:
            self.request.sendall(b"HTTP/1.1 404 Not Found\n")
        

    def parse_request(self, req):
        headers = {}
        lines = req.splitlines()
        inbody = False
        body = ''
        for line in lines[1:]:
            if line.strip() == "":
                inbody = True
            if inbody:
                body += line
            else:
                try:
                    k, v = line.split(":", 1)
                    headers[k.strip()] = v.strip()
                except ValueError as err:
                    print('Exception occurred while processing headers')
                
        method, path, _ = lines[0].split()
        self.path = path.lstrip("/")
        self.method = method
        self.headers = headers
        print(self.headers)
        self.body = body
        uri_request = ''
        parameter = ''
        if len(self.path) > 0:
            uri_request = self.path.split("/")[0]
        if '?' in uri_request:
            parameters = uri_request.split('?', 1)
            uri_request = parameters[0]
            parameters = parameters[1]
            parameter = parameters.split("=")[1]
        else:
            parameter = self.body
        return (uri_request, parameter)