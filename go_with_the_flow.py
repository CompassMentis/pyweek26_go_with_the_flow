import sys
import pygame

from settings import settings
from vehicle import Vehicles
from points import Points
from power_tower import PowerTowers
from map import Map

pygame.init()

size = width, height = 1600, 900

screen = pygame.display.set_mode(settings.size)

backgrounds = dict()
for i in range(4):
    backgrounds[i] = pygame.image.load(f'images/background_{i}.png')

points = Points()
with open('river_system.txt') as input_file:
    points.read(input_file)

power_towers = PowerTowers(screen)
power_towers.add(500, 500)
power_towers.add(800, 300)

vehicles = Vehicles(screen, points)
vehicles.add(100, 100)

map = Map(
    power_towers=power_towers,
    vehicles=vehicles,
)

background_index = 0
while 1:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        vehicles.turn(-1)

    if keys[pygame.K_RIGHT]:
        vehicles.turn(1)

    if keys[pygame.K_UP]:
        vehicles.faster()

    if keys[pygame.K_DOWN]:
        vehicles.slower()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PERIOD:
                vehicles.stop()

            if event.key == pygame.K_SPACE:
                vehicles.toggle_flow_mode()

    screen.blit(backgrounds[int(background_index)], (0, 0))
    background_index = background_index + 0.1
    if background_index > 3:
        background_index = 0

    power_towers.show()
    vehicles.show()

    pygame.display.flip()

    vehicles.move()
    power_towers.increase_charge()
    map.process_collisions()
