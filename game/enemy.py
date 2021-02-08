import ursina


class Enemy(ursina.Entity):
    def __init__(self, position):
        super().__init__(
            position=position,
            model="cube",
            origin_y=-0.5,
            collider="box",
            texture="white_cube",
            color=ursina.color.color(0, 0, 1),
            scale=ursina.Vec3(1, 2, 1)
        )

        gun = ursina.Entity(
            parent=self,
            position=ursina.Vec3(0.55, 0.5, 0.6),
            scale=ursina.Vec3(0.1, 0.2, 0.65),
            model="cube",
            texture="white_cube",
            color=ursina.color.color(0, 0, 0.4)
        )

        self.health = 100

    def update(self):
        color_saturation = 1 - self.health / 100
        self.color = ursina.color.color(0, color_saturation, 1)

        if self.health <= 0:
            ursina.destroy(self)
