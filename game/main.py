import ursina
from ursina.prefabs.first_person_controller import FirstPersonController

from floor import Floor

app = ursina.Ursina()

floor = Floor()
player = FirstPersonController(position=ursina.Vec3(0, 5, 0))
player.jump_height = 1.5
player.jump_duration = 0.65
player.cursor.color = ursina.color.rgb(255, 0, 0, 122)
player.origin_y = 2

app.run()
