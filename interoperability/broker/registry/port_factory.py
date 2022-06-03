from http.server import BaseHTTPRequestHandler
import socket
from socketserver import TCPServer
from config import INITAL_PORT, FINAL_PORT

class PortFactory():
    __local_used_ports = []
    def get_first_available_port(initial:int = INITAL_PORT, final:int = FINAL_PORT) -> int:
        for port in range(initial, final):
            try:
                with TCPServer(('', port), BaseHTTPRequestHandler) as s:
                    s.server_close()
                if port in PortFactory.__local_used_ports:
                    raise OSError()
                else:
                    PortFactory.__local_used_ports.append(port)
                return port
            except OSError:
                pass
        raise OSError(
            "All ports from {} to {} are in use. Please close a port.".format(
                initial, final
            )
        )

        