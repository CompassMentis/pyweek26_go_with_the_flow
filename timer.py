import os
from datetime import datetime

import pygame


class Timer:
    game_timer_location = (1502, 10)
    level_timer_location = (1502, 40)
    level_location = (1432, 36)

    def __init__(self, screen):
        self.start_time = datetime.now()
        self.level_time = self.start_time
        self.level = 0
        self.screen = screen

        self.digits_font = pygame.font.Font(os.path.join('fonts', '07-digit-font', 'digital-7.ttf'), 24)
        self.plain_font = pygame.font.SysFont('monospace', 24, bold=True)

    def next_level(self):
        self.level_time = datetime.now()
        self.level += 1

    @staticmethod
    def text_to_label(font, text):
        return font.render(text, 1, (80, 80, 80))

    def duration_to_label(self, duration):
        minutes = duration.seconds // 60
        seconds = duration.seconds % 60
        microseconds = duration.microseconds
        to_show = f'{minutes:02d}:{seconds:02d}.{(microseconds // 100000):01d}'
        return self.text_to_label(self.digits_font, to_show)

    def show(self):
        duration = datetime.now() - self.start_time

        label = self.duration_to_label(duration)
        self.screen.blit(label, self.game_timer_location)

        duration = datetime.now() - self.level_time
        label = self.duration_to_label(duration)
        self.screen.blit(label, self.level_timer_location)

        label = self.text_to_label(self.plain_font, str(self.level))
        self.screen.blit(label, self.level_location)
