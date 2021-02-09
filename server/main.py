"""
Server script for hosting games
"""

import socket
import json
import random
import threading

ADDR = "0.0.0.0"
PORT = 8000
MAX_PLAYERS = 10
MSG_SIZE = 2048

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


def handle_messages(identifier: str):
    client_info = players[identifier]
    conn: socket.socket = client_info["socket"]
    username = client_info["username"]

    while True:
        msg = conn.recv(MSG_SIZE)

        if not msg:
            break

        msg_decoded = msg.decode("utf8")
        msg_json = json.loads(msg_decoded)
        print(f"Received message from player {username} with ID {identifier}")

        players[identifier]["position"] = msg_json["position"]
        players[identifier]["rotation"] = msg_json["rotation"]

        for player_id in players:
            if player_id != identifier:
                player_info = players[player_id]
                player_conn: socket.socket = player_info["socket"]
                try:
                    player_conn.sendall(msg)
                except OSError:
                    pass

    print(f"Player {username} with ID {identifier} has left the game...")
    conn.close()


def main():
    print("Server started, listening for new connections...")

    while True:
        # Accept new connection and assign unique ID
        conn, addr = s.accept()
        new_id = generate_id(players, MAX_PLAYERS)
        conn.send(new_id.encode("utf8"))
        username = conn.recv(MSG_SIZE).decode("utf8")
        players[new_id] = {"socket": conn, "username": username, "position": (0, 0, 0), "rotation": 0}

        # Start thread to recieve messages from client
        msg_thread = threading.Thread(target=handle_messages, args=(new_id,), daemon=True)
        msg_thread.start()

        print(f"New connection from {addr}, assigned ID: {new_id}...")


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
