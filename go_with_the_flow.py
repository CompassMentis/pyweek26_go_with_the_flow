import sys
import pygame

from settings import settings
from vehicle import Vehicle
from points import Points
from power_tower import PowerTower

pygame.init()

size = width, height = 1600, 900

screen = pygame.display.set_mode(settings.size)

backgrounds = dict()
for i in range(4):
    backgrounds[i] = pygame.image.load(f'screenshot_{i}.png')

points = Points()
with open('river_system.txt') as input_file:
    points.read(input_file)

vehicle = Vehicle(screen, points, 100, 100)

power_tower = PowerTower(screen, 500, 100)

background_index = 0
while 1:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        vehicle.turn(-1)

    if keys[pygame.K_RIGHT]:
        vehicle.turn(1)

    if keys[pygame.K_UP]:
        vehicle.faster()

    if keys[pygame.K_DOWN]:
        vehicle.slower()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PERIOD:
                vehicle.stop()

            if event.key == pygame.K_SPACE:
                vehicle.toggle_flow_mode()

    screen.blit(backgrounds[int(background_index)], (0, 0))
    background_index = background_index + 0.1
    if background_index > 3:
        background_index = 0

    vehicle.show()
    power_tower.show()

    pygame.display.flip()

    vehicle.move()
    power_tower.increase_charge()