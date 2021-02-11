import random
import ursina


class Bullet(ursina.Entity):
    def __init__(self, position: ursina.Vec3, direction: float, x_direction: float, damage: int = random.randint(10, 25)):
        speed = 35
        dir_rad = ursina.math.radians(direction)
        x_dir_rad = ursina.math.radians(x_direction)

        self.velocity = ursina.Vec3(
            ursina.math.sin(dir_rad) * ursina.math.cos(x_dir_rad),
            ursina.math.sin(x_dir_rad),
            ursina.math.cos(dir_rad) * ursina.math.cos(x_dir_rad)
        ) * speed

        super().__init__(
            position=position + self.velocity / speed,
            model="sphere",
            collider="box",
            scale=0.2
        )

        self.damage = damage
        self.direction = direction
        self.x_direction = x_direction

    def update(self):
        self.position += self.velocity * ursina.time.dt

        hit_info = self.intersects()

        if hit_info.hit:
            for entity in hit_info.entities:
                try:
                    entity.health -= self.damage
                except AttributeError:
                    pass

            ursina.destroy(self)
