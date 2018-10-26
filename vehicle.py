import pygame
import math
from settings import settings


class Vehicles:
    def __init__(self, screen, points):
        self.screen = screen
        self.points = points
        self.vehicles = []
        self.current = None

    def add(self, x, y):
        self.current = Vehicle(self.screen, self.points, x, y)
        self.vehicles.append(self.current)

    def show(self):
        for vehicle in self.vehicles:
            vehicle.show()

    def move(self):
        for vehicle in self.vehicles:
            vehicle.move()

    def turn(self, direction):
        self.current.turn(direction)

    def faster(self):
        self.current.faster()

    def slower(self):
        self.current.slower()

    def stop(self):
        self.current.stop()

    def toggle_flow_mode(self):
        self.current.toggle_flow_mode()


class Vehicle:
    # The centre of the steering axle - the point around which the car should rotate
    pivot_point = (22, 40)
    max_rotation = 1
    max_charge = 5000

    def __init__(self, screen, points, x, y):
        self.x, self.y = x, y
        self.screen = screen
        self.points = points
        self.direction = 90
        self.speed = 2
        self.delta = 2, 2
        self.image_ready_to_flow = pygame.image.load('images/vehicle_ready_to_flow.png')
        self.image_ready_to_flow_empty = pygame.image.load('images/vehicle_ready_to_flow_empty.png')
        self.image_flowing = pygame.image.load('images/vehicle_flowing.png')
        self.image_driving = pygame.image.load('images/vehicle_driving.png')
        self.image_empty = pygame.image.load('images/vehicle_empty.png')
        self.image = None
        self.flow_mode = False
        self.image_offset = None
        self.point = None
        self.charge = 5000

        self.orientate()

    @property
    def original_image(self):
        if self.point:
            return self.image_flowing

        if self.flow_mode:
            if self.charge:
                return self.image_ready_to_flow
            else:
                return self.image_ready_to_flow_empty

        if self.charge:
            return self.image_driving

        return self.image_empty

    def show(self):
        self.screen.blit(self.image, (self.x + self.image_offset[0], self.y + self.image_offset[1]))

        pygame.draw.arc(
            self.screen,
            (0, 0, 163, 127),
            (self.x + self.image_offset[0], self.y + self.image_offset[1], 50, 50),
            math.radians(0),
            math.radians(359 * self.charge / self.max_charge),
            5
        )

    def orientate(self):
        """
        Set delta (x and y), based on direction and speed
        Also orientate the image to match the direction
        """

        radians_direction = math.radians(self.direction)

        self.delta = \
            math.sin(radians_direction) * self.speed, \
            -math.cos(radians_direction) * self.speed

        old_centre = self.original_image.get_rect().center

        pivot_point_to_old_centre = (
                old_centre[0] - self.pivot_point[0],
                old_centre[1] - self.pivot_point[1]
        )

        self.image = pygame.transform.rotate(self.original_image, 360 - self.direction)

        pivot_point_to_new_centre = (
            pivot_point_to_old_centre[0] * math.cos(radians_direction) - pivot_point_to_old_centre[1] * math.sin(radians_direction),
            pivot_point_to_old_centre[0] * math.sin(radians_direction) + pivot_point_to_old_centre[1] * math.cos(radians_direction)
        )
        new_centre = self.image.get_rect().center
        new_pivot_point = (
            new_centre[0] - pivot_point_to_new_centre[0],
            new_centre[1] - pivot_point_to_new_centre[1]
        )
        self.image_offset = (-new_pivot_point[0], -new_pivot_point[1])

    def turn(self, direction):
        """
        direction > 0 (left arrow key): clockwise, 45 degrees
        direction < 0 (right arrow key): counter clockwise, 45 degrees,
        """
        if direction > 0:
            self.direction += settings.turn_angle % 360
        else:
            self.direction -= settings.turn_angle % 360
        self.orientate()

    def faster(self):
        self.speed = min(self.speed + settings.speed_increase, settings.maximum_speed)
        self.orientate()

    def slower(self):
        self.speed = max(self.speed - settings.speed_increase, 0)
        self.orientate()

    def stop(self):
        self.speed = 0
        self.orientate()

    def toggle_flow_mode(self):
        if self.flow_mode:
            self.point = False
        self.flow_mode = not self.flow_mode
        self.orientate()

    def check_boundaries(self):
        # If car moved outside boundaries, put it back inside
        self.x = min(max(5, self.x), settings.map_width - self.image.get_width())
        self.y = min(max(5, self.y), settings.height - self.image.get_height())

    def steer_towards(self, new_direction):
        # Make sure both are >= 0, < 360
        self.direction = self.direction % 360
        new_direction = new_direction % 360

        # Go from A to B
        a = self.direction
        b = new_direction

        # Four different scenarios
        if a < b:
            # 0, A, B, 360, A' (A+360)

            if b - a < (a + 360) - b:
                # A to B less than B to A'
                # Shortest angle, clockwise
                angle = b - a
            else:
                # B to A' less than A to B
                # counter clockwise
                angle = a + 360 - b
        else:
            # 0, B, A, 360, B' (B+360)
            if a - b < (b + 360) - a:
                # B to A less than A to B'
                # shortest angle, counter clockwise
                angle = b - a
            else:
                angle = b + 360 - a

        if abs(angle) > self.max_rotation:
            if angle < 0:
                angle = -self.max_rotation
            else:
                angle = self.max_rotation
        # if self.direction < 0:
        #     self.direction += 360
        # if new_direction < 0:
        #     new_direction += 360

        # if abs(self.direction - new_direction) > self.max_rotation:
        #     if self.direction < new_direction:
        #         self.direction += self.max_rotation
        #     else:
        #         self.direction -= self.max_rotation
        # else:
        #     self.direction = new_direction
        self.direction = (self.direction + angle) % 360

    def move(self):
        if self.point:
            self.point = self.point.next
            if self.point:
                self.x, self.y = self.point.x, self.point.y
                self.steer_towards(self.point.angle)
            else:
                self.flow_mode = False
        else:
            # One step at a time, see if we hit the points
            delta_x, delta_y = self.delta

            if self.flow_mode:
                while abs(delta_x + delta_y) > 0.01 and not self.point and self.charge:
                    step_x, step_y = min(1, delta_x), min(1, delta_y)
                    self.x += step_x
                    self.y += step_y
                    delta_x -= step_x
                    delta_y -= step_y

                    # Use some power
                    self.charge -= math.sqrt(step_x**2 + step_y**2)
                    if self.charge < 0:
                        self.charge = 0

                    if self.points.contains(int(self.x), int(self.y)):
                        self.point = self.points.points[(int(self.x), int(self.y))]

                    self.check_boundaries()

            elif self.charge:
                self.x += delta_x
                self.y += delta_y
                self.charge -= math.sqrt(delta_x ** 2 + delta_y ** 2)
                self.check_boundaries()

        self.orientate()

    def charge_up(self, power_tower):
        capacity = self.max_charge - self.charge
        available = power_tower.charge * power_tower.charge_multiplier
        transfer = min(capacity, available)
        self.charge += transfer
        power_tower.charge -= transfer // power_tower.charge_multiplier
