import sys, os
sys.path.append(f"{os.getcwd()}/interoperability/core")
from protocol.model.message import Message
from protocol.http.handler import HttpRequestHandler
from protocol.http.serve import HTTPServe
from protocol.tcp.handler import TcpRequestHandler
from protocol.tcp.serve import TCPServe
from uris.identifier import URIIdentifier