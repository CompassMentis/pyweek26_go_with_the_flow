import pygame


class PowerTowers:
    def __init__(self, screen):
        self.towers = []
        self.screen = screen

    def reset(self):
        self.towers = []

    def add(self, x, y):
        self.towers.append(PowerTower(self.screen, x, y))

    def show(self):
        for t in self.towers:
            t.show()

    def increase_charge(self):
        for t in self.towers:
            t.increase_charge()


class PowerTower:
    STARTING_CHARGE = 0
    CHARGE_INCREASE = 0.1
    MAX_CHARGE = 100
    charge_multiplier = 50  # One charge moves the car 50 forward

    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.charge = self.STARTING_CHARGE
        self.screen = screen

        self.image_low = pygame.image.load('images/power_tower_low.png')
        self.image_medium = pygame.image.load('images/power_tower_medium.png')
        self.image_high = pygame.image.load('images/power_tower_high.png')

        self.image_ring = pygame.image.load('images/power_tower_ring.png')

    def increase_charge(self):
        self.charge = min(self.charge + self.CHARGE_INCREASE, self.MAX_CHARGE)

    def show(self):
        if self.charge > 80:
            image = self.image_high
        elif self.charge > 10:
            image = self.image_medium
        else:
            image = self.image_low
        self.screen.blit(image, (self.x, self.y))

        for i in range(int(self.charge)):
            self.screen.blit(self.image_ring, (self.x + 17, self.y + 46 - (i/3.3)))
