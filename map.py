from sounds import sounds

def image_collision(image_a, location_a, image_b, location_b):
    rect_a = image_a.get_rect().move(location_a)
    rect_b = image_b.get_rect().move(location_b)
    return rect_a.colliderect(rect_b)


class Map:
    def __init__(self, screen, power_towers, vehicles, destinations, hotels, travellers):
        self.screen = screen
        self.power_towers = power_towers
        self.vehicles = vehicles
        self.destinations = destinations
        self.hotels = hotels
        self.travellers = travellers

    def travellers_in_hotel(self, hotel):
        # For a given hotel, give a list of all travellers which it currently contains,
        # ignoring any which are done for the day
        return [t for t in self.travellers.things if t.location == hotel and not t.done]

    @property
    def travellers_outside_any_hotel(self):
        # Return the first current occupant (if any) for each hotel
        result = []
        for hotel in self.hotels.things:
            travellers = self.travellers_in_hotel(hotel)
            if travellers:
                result.append(travellers[0])
        return result

    def show(self):
        # Travellers outside a hotel
        # For each hotel, get list of travellers in it, then show the first one
        for traveller in self.travellers_outside_any_hotel:
            self.screen.blit(traveller.image, (traveller.hotel.x - 20, traveller.hotel.y))

    def vehicle_passenger(self, vehicle):
        for traveller in self.travellers.things:
            if traveller.location == vehicle:
                return traveller
        return None

    def process_collisions(self):
        for vehicle in self.vehicles.vehicles:
            # Vehicles with power tower - should we recharge?
            for power_tower in self.power_towers.towers:
                if image_collision(
                        vehicle.image, (vehicle.x, vehicle.y),
                        power_tower.image_medium, (power_tower.x, power_tower.y)
                ):
                    if vehicle.charge_up(power_tower) > 10:
                        sounds.play('charge_up')

            # Vehicles with passengers waiting outside a hotel
            passenger = self.vehicle_passenger(vehicle)
            if passenger is None:
                for traveller in self.travellers_outside_any_hotel:
                        if image_collision(
                            traveller.image, (traveller.hotel.x, traveller.hotel.y),
                            vehicle.image, (vehicle.x, vehicle.y)
                        ):
                            traveller.location = vehicle
                            sounds.play('passenger_collected')

            elif not passenger.done:
                yet_to_visit = passenger.yet_to_visit
                # Clash with a destination, when vehicle has a passenger
                for destination in yet_to_visit:
                    if image_collision(
                            destination.image, (destination.x, destination.y),
                            vehicle.image, (vehicle.x, vehicle.y)
                    ):
                        passenger.visited.append(destination)
                        sounds.play('arrived')

                # Passenger which has visited everything, collision with their hotel
                if not yet_to_visit:
                    if image_collision(
                            passenger.hotel.image, (passenger.hotel.x, passenger.hotel.y),
                            vehicle.image, (vehicle.x, vehicle.y)
                    ):
                        passenger.location = passenger.hotel
                        sounds.play('traveller_done')
