from datetime import datetime
import pygame


class Timer:
    game_timer_location = (1430, 15)

    def __init__(self, screen):
        self.start_time = datetime.now()
        self.level_time = self.start_time
        self.levels = 1
        self.screen = screen

        self.font = pygame.font.Font('fonts/01-digit-font/01 Digit.ttf', 24)

    def next_level(self):
        self.level_time = datetime.now()
        self.levels += 1

    def show(self):
        duration = datetime.now() - self.start_time

        minutes = duration.seconds // 60
        seconds = duration.seconds % 60
        microseconds = duration.microseconds

        to_show = f'{minutes:02d}:{seconds:02d}.{(microseconds // 100000):01d}'

        label = self.font.render(to_show, 1, (80, 80, 80))
        self.screen.blit(label, self.game_timer_location)
