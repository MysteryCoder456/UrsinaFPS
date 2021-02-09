"""
Server script for hosting games
"""

import socket
import random
import threading

ADDR = "0.0.0.0"
PORT = 8000
MAX_PLAYERS = 10

# Setup server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ADDR, PORT))
s.listen(MAX_PLAYERS)

players = {}


def generate_id(player_list: dict, max_players: int):
    """
    Generate a unique identifier

    Args:
        player_list (dict): dictionary of existing players
        max_players (int): maximum number of players allowed

    Returns:
        str: the unique identifier
    """

    while True:
        unique_id = str(random.randint(1, max_players))
        if unique_id not in player_list:
            return unique_id


def new_connection():
    while True:
        conn, addr = s.accept()
        new_id = generate_id(players, MAX_PLAYERS)
        print(f"New connection from {addr}, assigned ID: {new_id}...")
        conn.send(new_id.encode("utf8"))


def main():
    pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except SystemExit:
        pass
    finally:
        print("Exiting")
        s.close()
