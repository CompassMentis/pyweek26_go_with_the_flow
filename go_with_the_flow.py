import sys
import pygame
from random import choice

from settings import settings
from vehicle import Vehicle
from points import Points

pygame.init()

size = width, height = 1600, 900

screen = pygame.display.set_mode(settings.size)

# background = pygame.image.load('images/background.png')
backgrounds = dict()
for i in range(4):
    backgrounds[i] = pygame.image.load(f'screenshot_{i}.png')

points = Points()
with open('river_system.txt') as input_file:
    points.read(input_file)

vehicle = Vehicle(screen, points, 100, 100)

# points.list_segments()

# ps = []
# for _ in range(50):
#     ps.append(choice(list(points.points.values())))
ps = points.start_points

background_index = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                vehicle.turn(-1)

            if event.key == pygame.K_RIGHT:
                vehicle.turn(1)

            if event.key == pygame.K_UP:
                vehicle.faster()

            if event.key == pygame.K_DOWN:
                vehicle.slower()

            if event.key == pygame.K_PERIOD:
                vehicle.stop()

            if event.key == pygame.K_SPACE:
                vehicle.toggle_flow_mode()

    screen.blit(backgrounds[int(background_index)], (0, 0))
    background_index = background_index + 0.1
    if background_index > 3:
        background_index = 0
    # for y, x in points.points:
    #     pygame.draw.line(screen, (0, 0, 255), (x, y), (x, y))
    # vehicle.x, vehicle.y = p.x, p.y
    vehicle.show()

    # for p in ps:
    #     pygame.draw.circle(screen, (0, 0, 255), (p.x, p.y), 5)
    #
    # ps = [p.next for p in ps if p.next]
    #     # if p.next:
    #     #     p = p.next
    pygame.display.flip()

    vehicle.move()
