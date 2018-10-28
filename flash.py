import pygame

from draw_text import draw_text


class Flash:
    x = 15
    y = 15

    def __init__(self, screen):
        self.message = None
        self.timer = 0
        self.screen = screen

    def start(self, message):
        self.message = message
        self.timer = 500

    def show(self):
        if self.timer > 0:
            pygame.draw.rect(self.screen, (255, 255, 255, 127), (self.x, self.y, 1300, 25))
            draw_text.draw(self.screen, self.x + 5, self.y + 2, self.message)

        self.timer -= 1
