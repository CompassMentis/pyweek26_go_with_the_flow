import os

import pygame

pygame.mixer.pre_init(44100, 16, 2, 4096)


class Sounds:
    def __init__(self):
        self.sounds = dict()

    def play(self, name):
        if name not in self.sounds:
            filename = dict(
                arrived='gold-2.wav',
                passenger_collected='17.ogg',
                traveller_done='glassbell.wav',
                charge_up='gold-3.wav',
                retire_car='boss-shoot.wav',
            )[name]

            self.sounds[name] = pygame.mixer.Sound(os.path.join('sounds', filename))
        self.sounds[name].play()


# Todo: Don't use singletons?
sounds = Sounds()
