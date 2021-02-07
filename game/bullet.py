import ursina


class Bullet(ursina.Entity):
    def __init__(self, position: ursina.Vec3, direction: float):
        speed = 0.5
        self.velocity = ursina.Vec3(
            ursina.math.sin(ursina.math.radians(direction)),
            0,
            ursina.math.cos(ursina.math.radians(direction))
        ) * speed

        super().__init__(
            position=position + self.velocity / speed,
            model="sphere",
            collider="sphere",
            scale=0.2
        )

    def update(self):
        self.position += self.velocity
