import sys
import pygame

from settings import settings
from vehicle import Vehicles
from points import Points
from power_tower import PowerTowers
from map import Map
from destination import Destinations
from hotel import Hotels
from traveller import Travellers
from timer import Timer
from levels import Levels

# To do: Don't use singletons?
from queue import queue

pygame.init()

size = width, height = 1600, 900

screen = pygame.display.set_mode(settings.size)

backgrounds = dict()
for i in range(4):
    backgrounds[i] = pygame.image.load(f'images/background_{i}.png')

points = Points()
with open('river_system.txt') as input_file:
    points.read(input_file)

levels = Levels('levels.txt')

power_towers = PowerTowers(screen)
# power_towers.add(874, 174)
# power_towers.add(333, 370)

vehicles = Vehicles(screen, points)
# vehicles.add('red', 100, 100)
# vehicles.add('blue', 100, 150)
# vehicles.add('yellow', 100, 200)

destinations = Destinations(screen)
# totem = destinations.add('totem', 146, 107)
# mountain = destinations.add('mountain', 335, 470)
# deer = destinations.add('deer', 527, 682)
# hut = destinations.add('hut', 1056, 632)
# stone_circle = destinations.add('stone_circle', 1116, 551)

hotels = Hotels(screen)
# green_hotel = hotels.add('green_hotel', 1013, 187)
# old_hotel = hotels.add('old_hotel', 1275, 296)

travellers = Travellers(screen)

# traveller01 = travellers.add('traveller01', 0, 0)
# traveller01.hotel = green_hotel
# traveller01.location = green_hotel
# traveller01.plan = [hut]
#
# traveller02 = travellers.add('traveller02', 0, 0)
# traveller02.hotel = old_hotel
# traveller02.location = old_hotel
# traveller02.plan = [stone_circle]
#
# traveller03 = travellers.add('traveller03', 0, 0)
# traveller03.hotel = green_hotel
# traveller03.location = green_hotel
# traveller03.plan = [totem]
#
# traveller04 = travellers.add('traveller04', 0, 0)
# traveller04.hotel = green_hotel
# traveller04.location = green_hotel
# traveller04.plan = [deer, mountain]

def level_done():
    pass

map = Map(
    screen=screen,
    power_towers=power_towers,
    vehicles=vehicles,
    destinations=destinations,
    hotels=hotels,
    travellers=travellers,
)

timer = Timer(screen)
level = 0

background_index = 0
while 1:

    if not level or level_done():
        level += 1
        levels.switch(
            level,
            power_towers=power_towers,
            vehicles=vehicles,
            destinations=destinations,
            hotels=hotels,
            travellers=travellers
        )

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

            if event.key == pygame.K_TAB:
                vehicles.next()

            if vehicles.current:
                # print('Pressed: ', chr(event.key))
                for p in vehicles.current.upstream_points:
                    if chr(event.key).lower() == p.upstream_point_code.lower():
                        vehicles.current.move_upstream_to(p)

    screen.blit(backgrounds[int(background_index)], (0, 0))
    background_index = background_index + 0.1
    if background_index > 3:
        background_index = 0

    power_towers.show()
    destinations.show()
    hotels.show()
    travellers.show()
    map.show()
    timer.show()

    vehicles.show()

    pygame.display.flip()

    vehicles.move()
    power_towers.increase_charge()
    map.process_collisions()
    queue.tick()
