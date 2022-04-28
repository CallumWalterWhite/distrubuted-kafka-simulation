import datetime
import email
import html
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
import io
import mimetypes
import os
import posixpath
import shutil
import sys
import urllib.parse
from interoperability.broker.controller.controllerService import ControllerService



class RequestHandler(BaseHTTPRequestHandler):
    __controller: ControllerService

    def __init__(self, *args, controller=None, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = os.fspath(directory)
        super().__init__(*args, **kwargs)
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode("utf-8")
        self.parse_request(self.data)
        #func, args = self.path.split("/", 1)
        #args = args.split("/")
        #resp = getattr(self, func)(*args)
        self.server.callback(self.body)
        self.request.sendall(b"HTTP/1.1 200 OK\n")
        self.request.sendall(b"\n")
        #self.request.sendall(resp)

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
        #self.path, self.query_string = self.path.split("?", 1)
