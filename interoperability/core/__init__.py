import sys, os
sys.path.append(f"{os.getcwd()}\interoperability\core")
from handler.http_handler import HTTPHandler
from handler.request_handler import RequestHandler
from uris.identifier import URIIdentifier