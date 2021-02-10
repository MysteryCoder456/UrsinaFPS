import sys
import socket
import threading
import ursina
from network import Network

from floor import Floor
from player import Player
from enemy import Enemy
from bullet import Bullet


def valid_addr(ip, port):
    valid = True

    if len(ip.split(".")) != 4:
        valid = False

    try:
        _ = int(port)
    except ValueError:
        valid = False

    return valid


username = input("Enter your username: ")

while True:
    server_addr = input("Enter server IP: ")
    server_port = input("Enter server port: ")

    if valid_addr(server_addr, server_port):
        server_port = int(server_port)
        n = Network(server_addr, server_port, username)
        n.settimeout(5)

        error_occurred = False

        try:
            n.connect()
        except ConnectionRefusedError:
            print("Connection refused! This can be because server hasn't started or has reached player limit.")
            error_occurred = True
        except socket.timeout:
            print("Server took too long to respond, please try again...")
            error_occurred = True
        finally:
            n.settimeout(None)

        if error_occurred:
            continue

        break

    print("\nThe server information you entered was invalid, please try again...")


app = ursina.Ursina()
ursina.window.borderless = False
ursina.window.title = "Ursina FPS"
ursina.window.exit_button.visible = False

floor = Floor()
player = Player(ursina.Vec3(0, 1, 0))
prev_pos = player.world_position
prev_dir = player.world_rotation_y
enemies = []


def receive():
    while True:
        try:
            info = n.receive_info()
        except Exception as e:
            print(e)
            continue

        if not info:
            print("Server has stopped! Exiting...")
            sys.exit()

        if info["object"] == "player":
            enemy_id = info["id"]

            if info["joined"]:
                new_enemy = Enemy(ursina.Vec3(*info["position"]), enemy_id, info["username"], player)
                enemies.append(new_enemy)
                continue

            enemy = None

            for e in enemies:
                if e.id == enemy_id:
                    enemy = e
                    break

            if not enemy:
                continue

            if info["left"]:
                enemies.remove(enemy)
                ursina.destroy(enemy)
                continue

            enemy.world_position = ursina.Vec3(*info["position"])
            enemy.rotation_y = info["rotation"]

        elif info["object"] == "bullet":
            b_pos = ursina.Vec3(*info["position"])
            b_dir = info["direction"]
            b_x_dir = info["x_direction"]
            new_bullet = Bullet(b_pos, b_dir, b_x_dir)
            ursina.destroy(new_bullet, delay=2)


def update():
    global prev_pos, prev_dir

    if prev_pos != player.world_position or prev_dir != player.world_rotation_y:
        n.send_info(player)

    prev_pos = player.world_position
    prev_dir = player.world_rotation_y


def input(key):
    if key == "left mouse down":
        b_pos = player.position + ursina.Vec3(0, 2, 0)
        bullet = Bullet(b_pos, player.world_rotation_y, -player.camera_pivot.world_rotation_x)
        n.send_bullet(bullet)
        ursina.destroy(bullet, delay=2)


msg_thread = threading.Thread(target=receive, daemon=True)
msg_thread.start()
app.run()
