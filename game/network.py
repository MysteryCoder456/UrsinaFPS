import socket
import json

from player import Player


class Network:
    """
    A client class to abstract away socket functions and make communication with server less of a headache.

    Args:
        server_addr (str): IPv4 address of the server
        server_port (int): Port at which server is running
        username (str): Username of this client's player
    """

    def __init__(self, server_addr: str, server_port: int, username: str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = server_addr
        self.port = server_port
        self.username = username
        self.recv_size = 2048
        self.id = 0

    def connect(self):
        """
        Connect to the server and get the ID assigned to this client

        Returns:
            str: unique ID assigned to this client
        """

        self.client.connect((self.addr, self.port))
        self.id = self.client.recv(self.recv_size).decode("utf8")
        self.client.send(self.username.encode("utf8"))

    def send_info(self, player: Player):
        player_info = {
            "id": self.id,
            "position": (player.x, player.y),
            "rotation": (player.world_rotation_y)
        }
        player_info_encoded = json.dumps(player_info).encode("utf8")

        try:
            self.client.sendall(player_info_encoded)
        except socket.error as e:
            print(e)
