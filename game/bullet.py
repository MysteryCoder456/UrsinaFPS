import random
import ursina

from enemy import Enemy


class Bullet(ursina.Entity):
    def __init__(self, position: ursina.Vec3, direction: float, x_direction: float):
        speed = 0.5
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
            collider="sphere",
            scale=0.2
        )

        self.damage = random.randint(10, 25)

    def update(self):
        self.position += self.velocity

        hit_info = self.intersects()

        if hit_info.hit:
            for entity in hit_info.entities:
                if isinstance(entity, Enemy):
                    entity.health -= self.damage

            ursina.destroy(self)
