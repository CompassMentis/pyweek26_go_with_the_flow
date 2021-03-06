import os
import math

import pygame

from queue import queue
from sounds import sounds
from draw_text import draw_text
from settings import settings


class Vehicles:
    def __init__(self, screen, points):
        self.screen = screen
        self.points = points
        self.vehicles = []
        self.current_id = None

    def reset(self):
        self.vehicles = []
        self.current_id = None

    @property
    def all_gone(self):
        for vehicle in self.vehicles:
            if not vehicle.retired:
                return False
        return True

    def add(self, colour, x, y):
        vehicle = Vehicle(self.screen, self.points, colour, x, y)
        self.vehicles.append(vehicle)
        self.current_id = 0
        self.vehicles[0].active = True
        return vehicle

    @property
    def current(self):
        return self.vehicles[self.current_id]

    def next(self):
        self.current_id += 1
        if self.current_id >= len(self.vehicles):
            self.current_id = 0
        for i, vehicle in enumerate(self.vehicles):
            vehicle.active = (i == self.current_id)
        return self.current

    def show(self):
        # Todo: Probably don't need to do this every time - but only when something actually retired
        current = self.vehicles[self.current_id]
        self.vehicles = [v for v in self.vehicles if not v.retired]

        if not self.vehicles:
            return

        self.current_id = 0
        for i, v in enumerate(self.vehicles):
            if v == current:
                self.current_id = i

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

    def __init__(self, screen, points, colour, x, y):
        self.x, self.y = x, y
        self.screen = screen
        self.points = points
        self.direction = 90
        self.speed = 0
        self.delta = 0, 0
        self.colour_name = colour
        self.image_ready_to_flow = pygame.image.load(os.path.join('images', f'vehicle_{colour}', 'vehicle_ready_to_flow.png'))
        self.image_ready_to_flow_empty = pygame.image.load(os.path.join('images', f'vehicle_{colour}', 'vehicle_ready_to_flow_empty.png'))
        self.image_flowing = pygame.image.load(os.path.join('images', f'vehicle_{colour}', 'vehicle_flowing.png'))
        self.image_driving = pygame.image.load(os.path.join('images', f'vehicle_{colour}', 'vehicle_driving.png'))
        self.image_empty = pygame.image.load(os.path.join('images', f'vehicle_{colour}', 'vehicle_ready_to_flow_empty.png'))

        self.image = None
        self.flow_mode = False
        self.image_offset = None
        self.point = None
        self.charge = 1000
        self.active = False
        self.retiring = False
        self.retired = False
        self.upstream_points = []
        self.upstream_route = []

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

        if self.charge > 5:
            return self.image_driving

        return self.image_empty

    def show(self):
        self.screen.blit(self.image, (self.x + self.image_offset[0], self.y + self.image_offset[1]))

        colour = (0, 0, 163, 127) if self.active else (127, 127, 127, 127)

        if self.charge > 5:
            pygame.draw.arc(
                self.screen,
                colour,
                (self.x + self.image_offset[0], self.y + self.image_offset[1], 50, 50),
                math.radians(0),
                math.radians(359 * self.charge / self.max_charge),
                5
            )

        for i, p in enumerate(self.upstream_points):
            if self.upstream_route and p == self.upstream_route[0]:
                colour = (255, 127, 127, 127)
            else:
                colour = (127, 255, 127, 127)
            pygame.draw.circle(self.screen, colour, (p.x, p.y), 10)
            draw_text.draw(self.screen, p.x - 7, p.y - 12, p.upstream_point_code)

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
        # self.speed = 0
        self.upstream_route = []

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

    def set_upstream_points(self):
        self.upstream_points = []
        to_continue = [self.point]
        visited = set()
        while to_continue:
            p = to_continue.pop()
            while p is not None:
                if len(p.previous) == 2:
                    to_continue.append(p.previous[0])
                    p = p.previous[1]
                elif len(p.previous) == 1:
                    p = p.previous[0]
                else:
                    self.upstream_points.append(p)
                    p = None

                visited.add(p)

    def move_upstream_to(self, upstream_point):
        self.upstream_route = []
        p = upstream_point
        end_point = self.points.points[(self.x, self.y)]
        while p and p != end_point:
            self.upstream_route.append(p)
            p = p.next

    def move(self):
        if self.upstream_route:
            # Move upstream
            self.charge -= 2
            self.point = self.upstream_route.pop()
            self.steer_towards(self.point.angle + 180)
            self.x, self.y = self.point.x, self.point.y
            if self.upstream_route:
                self.set_upstream_points()
            else:
                self.point = None
                self.speed = 0
                self.flow_mode = False

            self.orientate()

        elif self.point:
            # Move downstream
            self.point = self.point.next
            if self.point:
                self.x, self.y = self.point.x, self.point.y
                self.steer_towards(self.point.angle)
                self.set_upstream_points()
            else:
                self.flow_mode = False
                self.charge = 0  # About to disappear
        else:
            self.upstream_points = []
            # Drive

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

            elif self.charge > 0:
                self.x += delta_x
                self.y += delta_y
                self.charge -= math.sqrt(delta_x ** 2 + delta_y ** 2)
                self.check_boundaries()

        if self.charge <= 0 and not self.retiring:
            queue.add(200, 'retire_car', self)
            self.retiring = True

        self.orientate()

    def charge_up(self, power_tower):
        capacity = self.max_charge - self.charge
        available = power_tower.charge * power_tower.charge_multiplier
        transfer = min(capacity, available)
        self.charge += transfer
        power_tower.charge -= transfer // power_tower.charge_multiplier

        return transfer

    def retire(self):
        self.retired = True
        sounds.play('retire_car')
