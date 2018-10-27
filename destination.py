from thing import Thing, Things


class Destination(Thing):
    folder = 'images/destinations'


class Destinations(Things):
    things_class = Destination
