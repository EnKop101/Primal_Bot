from Classes.rcon_class import RCON_Class
from rcon.source import Client
import socket

class RCON_Functions:
    def __init__(self, rcon_class: RCON_Class):
        self.rcon_class = rcon_class

    async def send_command(self, command: str):
        try:
            with Client(self.rcon_class.ip, self.rcon_class.port, passwd=self.rcon_class.password, timeout=3.0) as client:
                response = client.run(command)
            return response
        except socket.timeout as timeout:
            print("RCON Timeout: ", timeout)
            return None