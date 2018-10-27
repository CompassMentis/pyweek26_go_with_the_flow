from thing import Things, Thing


class Hotel(Thing):
    folder = 'images/hotels'


class Hotels(Things):
    things_class = Hotel
