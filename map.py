def image_collision(image_a, location_a, image_b, location_b):
    rect_a = image_a.get_rect().move(location_a)
    rect_b = image_b.get_rect().move(location_b)
    return rect_a.colliderect(rect_b)


class Map:
    def __init__(self, power_towers, vehicles):
        self.power_towers = power_towers
        self.vehicles = vehicles

    def process_collisions(self):
        for vehicle in self.vehicles.vehicles:
            for power_tower in self.power_towers.towers:
                if image_collision(
                        vehicle.image, (vehicle.x, vehicle.y),
                        power_tower.image_medium, (power_tower.x, power_tower.y)
                ):
                    vehicle.charge_up(power_tower)
