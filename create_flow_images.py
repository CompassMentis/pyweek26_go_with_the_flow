import sys
import pygame
from random import choice

from settings import settings
from points import Points

pygame.init()

size = width, height = 1600, 900

screen = pygame.display.set_mode(settings.size)

background = pygame.image.load('images/background.png')
circle_strong = pygame.image.load('images/river_circle_strong.png').convert_alpha()
circle_medium = pygame.image.load('images/river_circle_medium.png').convert_alpha()
circle_weak = pygame.image.load('images/river_circle_weak.png').convert_alpha()

points = Points()
with open('river_system.txt') as input_file:
    points.read(input_file)

# while 1:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
    for i in range(4):

        # screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        for p in points.points.values():
            if p.distance_to_end % 3:
                continue
            circle = {
                0: circle_strong,
                1: circle_medium,
                2: circle_weak,
                3: circle_medium
            }[((p.distance_to_end //3) +i )% 4]
            screen.blit(circle, (p.x - 3, p.y - 3))
        # for y, x in points.points:
        #     pygame.draw.line(screen, (0, 0, 255), (x, y), (x, y))
        # vehicle.x, vehicle.y = p.x, p.y
        # vehicle.show()

        # for p in ps:
        #     pygame.draw.circle(screen, (0, 0, 255), (p.x, p.y), 5)
        #
        # ps = [p.next for p in ps if p.next]
        #     # if p.next:
        #     #     p = p.next
        pygame.display.flip()

        # vehicle.move()
        pygame.image.save(screen, f'screenshot_{i}.png')