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
        self.parse_request(self.data)
        func = ''
        if len(self.path) > 0:
            func = self.path.split("/")[0]
        try:
            URIIdentifier.invoke_function(self.server.reflection_class, func, self.body)
            self.request.sendall(b"HTTP/1.1 200 OK\n")
        except:
            self.request.sendall(b"HTTP/1.1 404 Not Found\n")
        self.request.sendall(b"\n")
        

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
        self.body = body
