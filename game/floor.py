import ursina


class FloorCube(ursina.Entity):
    def __init__(self, position):
        super().__init__(
            position=position,
            scale=2,
            model="cube",
            texture="white_cube",
            collider="box"
        )


class Floor:
    def __init__(self):
        dark1 = True
        for z in range(-20, 20, 2):
            dark2 = not dark1
            for x in range(-20, 20, 2):
                cube = FloorCube(ursina.Vec3(x, 0, z))
                if dark2:
                    cube.color = ursina.color.color(0, 0, 0.8)
                dark2 = not dark2
            dark1 = not dark1
