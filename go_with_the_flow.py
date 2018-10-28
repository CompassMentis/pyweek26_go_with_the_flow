import sys
import os
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
from flash import Flash

# To do: Don't use singletons?
from queue import queue


def level_done(travellers):
    for traveller in travellers.things:
        if not traveller.done:
            return False
    return True


pygame.init()

size = width, height = 1600, 900

screen = pygame.display.set_mode(settings.size)

backgrounds = dict()
for i in range(4):
    backgrounds[i] = pygame.image.load(os.path.join('images', f'background_{i}.png'))

points = Points()
with open('river_system.txt') as input_file:
    points.read(input_file)

levels = Levels('levels.txt')

power_towers = PowerTowers(screen)
vehicles = Vehicles(screen, points)
destinations = Destinations(screen)
hotels = Hotels(screen)
travellers = Travellers(screen)
flash = Flash(screen)

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
done = False
while not done:

    if not level or level_done(travellers):
        level += 1
        if levels.all_done(level):
            done = True
            break

        timer.next_level()

        levels.switch(
            level,
            power_towers=power_towers,
            vehicles=vehicles,
            destinations=destinations,
            hotels=hotels,
            travellers=travellers,
            flash=flash,
        )

    if vehicles.all_gone:
        done = True
        break

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
    flash.show()

    vehicles.show()

    pygame.display.flip()

    vehicles.move()
    power_towers.increase_charge()
    map.process_collisions()
    queue.tick()

overlay_name = 'success_overlay' if levels.all_done(level) else 'game_over_overlay'
overlay = pygame.image.load(os.path.join('images', f'{overlay_name}.png'))

screen.blit(overlay, (0, 0))
pygame.display.flip()

# Wait for the space bar
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                done = True
