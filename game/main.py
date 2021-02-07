import ursina
from ursina.prefabs.first_person_controller import FirstPersonController

from floor import Floor

app = ursina.Ursina()

floor = Floor()
player = FirstPersonController(position=ursina.Vec3(-25, 5, -25))

app.run()
