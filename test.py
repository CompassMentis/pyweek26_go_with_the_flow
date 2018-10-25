import pygame

from settings import settings

pygame.init()

size = width, height = 1600, 900

screen = pygame.display.set_mode(settings.size)

pygame.draw.line(screen, (255, 0, 0), (0, 100), (700, 100))
pygame.draw.line(screen, (255, 0, 0), (100, 0), (100, 700))

vehicle = pygame.image.load('images/vehicle.png')
