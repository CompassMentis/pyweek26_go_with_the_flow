import pygame


def desaturate(image):
    result = image.copy()
    rect = result.get_rect()
    for i in range(rect[2]):
        for j in range(rect[3]):
            rgba = list(tuple(result.get_at((i, j))))
            level = sum(v for v in rgba[:3]) / 3
            for k in range(3):
                rgba[k] = level
            result.set_at((i, j), rgba)
    return result


class Thing:
    folder = 'images'
    extension = '.png'
    plan_image_height = 38

    def __init__(self, screen, name, x, y):
        self.screen = screen
        self.name = name
        self.x = x
        self.y = y
        self.image = pygame.image.load(f'{self.folder}/{self.name}{self.extension}')
        self._plan_image = None
        self._plan_image_desaturated = None
        self._image_desaturated = None

    def show(self):
        self.screen.blit(self.image, (self.x, self.y))

    @property
    def plan_image(self):
        if self._plan_image is None:
            _, _, w, h = self.image.get_rect()
            scaling_factor = self.plan_image_height / h
            w = int(w * scaling_factor)
            h = int(h * scaling_factor)
            self._plan_image = pygame.transform.scale(self.image, (w, h))
        return self._plan_image

    @property
    def plan_image_desaturated(self):
        if self._plan_image_desaturated is None:
            self._plan_image_desaturated = desaturate(self.plan_image)
        return self._plan_image_desaturated

    @property
    def image_desaturated(self):
        if self._image_desaturated is None:
            self._image_desaturated = desaturate(self.image)
        return self._image_desaturated


class Things:
    things_class = Thing

    def __init__(self, screen):
        self.things = []
        self.screen = screen

    def add(self, name, x, y):
        thing = self.things_class(self.screen, name, x, y)
        self.things.append(thing)
        return thing

    def show(self):
        for thing in self.things:
            thing.show()

    def get(self, name):
        for thing in self.things:
            if thing.name == name:
                return thing
        return None
