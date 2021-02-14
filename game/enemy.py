import ursina


class Enemy(ursina.Entity):
    def __init__(self, position: ursina.Vec3, identifier: str, username: str):
        super().__init__(
            position=position,
            model="cube",
            origin_y=-0.5,
            collider="box",
            texture="white_cube",
            color=ursina.color.color(0, 0, 1),
            scale=ursina.Vec3(1, 2, 1)
        )

        self.gun = ursina.Entity(
            parent=self,
            position=ursina.Vec3(0.55, 0.5, 0.6),
            scale=ursina.Vec3(0.1, 0.2, 0.65),
            model="cube",
            texture="white_cube",
            color=ursina.color.color(0, 0, 0.4)
        )

        self.name_tag = ursina.Text(
            parent=self,
            text=username,
            position=ursina.Vec3(0, 1.3, 0),
            scale=ursina.Vec2(5, 3),
            billboard=True,
            origin=ursina.Vec2(0, 0)
        )

        self.health = 100
        self.id = identifier
        self.username = username

    def update(self):
        try:
            color_saturation = 1 - self.health / 100
        except AttributeError:
            self.health = 100
            color_saturation = 1 - self.health / 100

        self.color = ursina.color.color(0, color_saturation, 1)

        if self.health <= 0:
            ursina.destroy(self)
