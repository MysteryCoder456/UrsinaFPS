import ursina


class Floor(ursina.Entity):
    def __init__(self):
        super().__init__(
            position=ursina.Vec3(-50, 0, -50),
            scale=ursina.Vec3(100, 1, 100),
            model="cube",
            texture="white_cube",
            collider="box"
        )
