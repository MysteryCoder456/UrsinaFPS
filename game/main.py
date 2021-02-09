import sys
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

        try:
            n.connect()
        except ConnectionRefusedError:
            print("Connection refused! This can be because server hasn't started or has reached player limit.")

        break

    print("\nThe server information you entered was invalid, please try again...")


app = ursina.Ursina()
ursina.window.borderless = False
ursina.window.title = "Ursina FPS"
ursina.window.exit_button.visible = False

floor = Floor()
player = Player(ursina.Vec3(0, 1, 0))
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

        enemy_id = info["id"]

        if info["joined"]:
            new_enemy = Enemy(ursina.Vec3(*info["position"]), enemy_id)
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


def update():
    n.send_info(player)


def input(key):
    if key == "left mouse down":
        b_pos = player.position + ursina.Vec3(0, 2, 0)
        bullet = Bullet(b_pos, player.world_rotation_y, -player.camera_pivot.world_rotation_x)
        ursina.destroy(bullet, delay=2)


msg_thread = threading.Thread(target=receive, daemon=True)
msg_thread.start()
app.run()
