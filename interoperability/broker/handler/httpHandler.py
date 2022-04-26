import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

async def startHandler(port):
    with TCPServer(("", port), SimpleHTTPRequestHandler) as httpd:
        print("serving at port", port)
        await httpd.serve_forever()