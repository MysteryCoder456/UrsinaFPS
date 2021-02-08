import ursina

from floor import Floor
from player import Player
from enemy import Enemy
from bullet import Bullet

app = ursina.Ursina()
ursina.window.borderless = False
ursina.window.title = "Ursina FPS"
ursina.window.exit_button.visible = False

floor = Floor()
e1 = Enemy(ursina.Vec3(0, 1, 5))
player = Player(ursina.Vec3(0, 1, 0))


def input(key):
    if key == "left mouse down":
        b_pos = player.position + ursina.Vec3(0, 2, 0)
        bullet = Bullet(b_pos, player.world_rotation_y, -player.camera_pivot.world_rotation_x)
        ursina.destroy(bullet, delay=2)


app.run()
