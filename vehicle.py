import pygame
import math
from settings import settings


class Vehicle:
    # The centre of the steering axle - the point around which the car should rotate
    pivot_point = (22, 40)

    def __init__(self, screen, points, x, y):
        self.x, self.y = x, y
        self.screen = screen
        self.points = points
        self.direction = 0
        self.speed = 2
        self.delta = 2, 2
        self.original_image = pygame.image.load('images/vehicle.png')
        self.image = None
        self.flow_mode = False
        self.image_offset = None
        self.orientate()
        self.point = None

    def show(self):
        self.screen.blit(self.image, (self.x + self.image_offset[0], self.y + self.image_offset[1]))
        # self.screen.blit(self.image, (self.x - self.image_offset[0], self.y - self.image_offset[1]))

        # try:
        #     self.screen.blit(self.image, (self.x + 300, self.y + 300))
        # except:
        #     pass

    def orientate(self):
        """
        Set delta (x and y), based on direction and speed
        Also orientate the image to match the direction
        """
        # loc = self.original_image.get_rect().center
        # self.image.get_rect().center = loc

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

    def move(self):
        if self.point:
            self.point = self.point.next
            if self.point:
                self.x, self.y = self.point.x, self.point.y
                self.direction = self.point.angle
                self.orientate()
            else:
                self.flow_mode = False
        else:
            self.x += self.delta[0]
            self.x = min(max(0, self.x), settings.width - self.image.get_width())
            self.y += self.delta[1]
            self.y = min(max(0, self.y), settings.height - self.image.get_height())
            if self.flow_mode:
                # Todo: swap x and y?
                if self.points.contains(int(self.x), int(self.y)):
                    self.point = self.points.points[(int(self.x), int(self.y))]
                    self.orientate()
