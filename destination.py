import os

from thing import Thing, Things


class Destination(Thing):
    folder = os.path.join('images', 'destinations')


class Destinations(Things):
    things_class = Destination
