from collections import defaultdict


class Level:
    def __init__(self, name):
        self.name = name
        self.data = defaultdict(list)


def remove_brackets(a):
    return a.replace('[', '').replace(']', '')


class Levels:
    def __init__(self, filename):
        self.levels = dict()
        self.load(filename)

    def load(self, filename):
        mode = None
        with open(filename) as input_file:
            for line in input_file.readlines():
                line = line.strip()
                if line.startswith('[level:'):
                    name = int(remove_brackets(line).replace('level:', '').strip())
                    level = Level(name)
                    self.levels[name] = level

                elif line.startswith('['):
                    mode = remove_brackets(line).strip()

                elif line.strip():
                    level.data[mode].append(line.strip())

    def switch(self, name, power_towers, vehicles, destinations, hotels, travellers, flash):
        level = self.levels[name]

        power_towers.reset()
        for line in level.data['power_towers']:
            x, y = line.split(',')
            x, y = int(x), int(y)
            power_towers.add(x, y)

        vehicles.reset()
        vehicles_idx = dict()
        for line in level.data['vehicles']:
            name, x, y = line.split(',')
            name, x, y = name.strip(), int(x), int(y)
            vehicles_idx[name] = vehicles.add(name, x, y)

        destinations.reset()
        destinations_idx = dict()
        for line in level.data['destinations']:
            name, x, y = line.split(',')
            name, x, y = name.strip(), int(x), int(y)
            destinations_idx[name] = destinations.add(name, x, y)

        hotels.reset()
        hotels_idx = dict()
        for line in level.data['hotels']:
            name, x, y = line.split(',')
            name, x, y = name.strip(), int(x), int(y)
            hotels_idx[name] = hotels.add(name, x, y)

        travellers.reset()
        for line in level.data['travellers']:
            name, hotel, raw_destinations = line.split(',')
            name, hotel = name.strip(), hotel.strip()
            plan = raw_destinations.split('>')
            plan = [d.strip() for d in plan]
            traveller = travellers.add(name, 0, 0)
            traveller.hotel = hotels_idx[hotel]
            traveller.location = hotels_idx[hotel]
            traveller.plan = [destinations_idx[p] for p in plan]

        if level.data['help']:
            line = level.data['help'][0].strip()
            flash.start(line)

    def all_done(self, level):
        return level not in self.levels
