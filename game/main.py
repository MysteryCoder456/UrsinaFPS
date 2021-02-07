import ursina
from ursina.prefabs.first_person_controller import FirstPersonController

from floor import Floor
from bullet import Bullet

app = ursina.Ursina()
ursina.window.borderless = False
ursina.window.title = "Ursina FPS"
ursina.window.exit_button.visible = False

floor = Floor()
player = FirstPersonController(
    position=ursina.Vec3(0, 5, 0),
    model="cube",
    jump_height=1.5,
    jump_duration=0.65,
    origin_y=-2
)
player.cursor.color = ursina.color.rgb(255, 0, 0, 122)


def input(key):
    print(key)
    if key == "left mouse down":
        b_pos = player.position + ursina.Vec3(0, 1.5, 0)
        bullet = Bullet(b_pos, player.world_rotation_y, -player.camera_pivot.world_rotation_x)
        ursina.destroy(bullet, delay=2)


app.run()
