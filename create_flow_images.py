import os

import pygame

from settings import settings
from points import Points

pygame.init()

size = width, height = 1600, 900

screen = pygame.display.set_mode(settings.size)

background = pygame.image.load(os.path.join('images', 'background.png'))
circle_strong = pygame.image.load(os.path.join('images', 'river_circle_strong.png')).convert_alpha()
circle_medium = pygame.image.load(os.path.join('images', 'river_circle_medium.png')).convert_alpha()
circle_weak = pygame.image.load(os.path.join('images', 'river_circle_weak.png')).convert_alpha()

points = Points()
with open('river_system.txt') as input_file:
    points.read(input_file)

    for i in range(4):

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
        pygame.display.flip()

        pygame.image.save(screen, os.path.join('images', f'background_{i}.png'))
