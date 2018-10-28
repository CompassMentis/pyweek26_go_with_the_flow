import os

from thing import Things, Thing


class Hotel(Thing):
    folder = os.path.join('images', 'hotels')


class Hotels(Things):
    things_class = Hotel
