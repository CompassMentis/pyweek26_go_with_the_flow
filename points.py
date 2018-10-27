START_VALUE = [255, 0, 0, 255]
MIDDLE_VALUE = [0, 0, 255, 255]
END_VALUE = [0, 255, 0, 255]
EMPTY_VALUE = [0, 0, 0, 255]


class Point:
    def __init__(self, x, y, d, angle):
        self.x = x
        self.y = y
        self.next = None
        self.end_point = False
        self.distance_to_end = d
        self.angle = angle
        self.previous = []
        self.upstream_point_code = None

    def __repr__(self):
        return f'{self.x}, {self.y}'

    def calculate_distance_to_end(self):
        p = self
        self.distance_to_end = 0
        while p.next:
            self.distance_to_end += 1
            p = p.next

    @property
    def serialised(self):
        return f'{self.y}, {self.x}, {self.distance_to_end}, {self.angle}'


class Points:
    def __init__(self):
        self.points = dict()
        self.current = None
        self.start_points = []
        self.end_points = []
        self.upstream_points = []

    def add_point(self, x, y, d=None, angle=None):
        # Point already exists, so don't create another one
        if self.contains(x, y):
            self.current.next = self.points[(x, y)]
            self.current = self.points[(x, y)]
            return

        next_point = Point(x, y, d, angle)
        self.points[(x, y)] = next_point
        if self.current:
            self.current.next = next_point
        else:
            self.start_points.append(next_point)
        self.current = next_point

    def next_segment(self):
        # Todo: Turn this into a set
        if self.current and self.current not in self.end_points:
            self.end_points.append(self.current)
            self.current.end_point = True
        self.current = None

    def contains(self, x, y):
        return (x, y) in self.points

    def link_segments(self, image):
        """
        For each end point, find the neighbouring start point, if any,
        and link the end point to the start point
        """
        for point in self.end_points:
            # print(f'Next point for {point.x}, {point.y}')
            x, y = point.x, point.y
            for i, j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                x2, y2 = x + i, y + j
                point_colour = list(image[x2, y2])
                if point_colour == START_VALUE:
                    point.next = self.points[(x2, y2)]
                    # print(f'Found at {x2}, {y2}')
                    break

    def write(self, output_file):
        # Todo: x and y are swapped in the rest of the code - fix this
        for point in self.start_points:
            p = point
            while p:
                output_file.write(f'{p.serialised}\n')
                if p.end_point:
                    if p.next:
                        output_file.write(f'>{p.next.serialised}\n')
                    else:
                        output_file.write('----\n')
                    break
                p = p.next

    def read(self, input_file):
        # Table of how to finish the connections
        next_points = dict()

        for line in input_file.readlines():
            if line.strip().startswith('----'):
                self.next_segment()
                continue

            x, y, d, angle = line.replace('>', '').strip().split(', ')
            x, y, d, angle = int(x), int(y), int(d), int(angle)
            if line.strip().startswith('>'):
                next_points[self.current] = (x, y)
                # start new segment
                self.next_segment()
            else:
                self.add_point(x, y, d, angle)

        for point, next_location in next_points.items():
            point.next = self.points[next_location]

        self.set_upstream_routes()

    def set_upstream_routes(self):
        # Travel down from each end point to the start
        # at each point, add a pointer from the next point back to itself
        for point in self.start_points:
            p = point
            while p.next:
                if p not in p.next.previous:
                    p.next.previous.append(p)
                p = p.next

        # Make a list of all the points with no previous points - i.e. the upstream route end points
        for point in self.start_points:
            if not point.previous:
                self.upstream_points.append(point)

        for i, point in enumerate(self.upstream_points):
            point.upstream_point_code = 'ABCDEFGHJKLMNOPQRSTUVWXYZ23456789£$%^&*()'[i]

    def list_segments(self):
        for point in self.start_points:
            p = point
            while p.next:
                p = p.next
            print(f'Segment from {point.x}, {point.y} to {p.x}, {p.y}')

    def calculate_distances_to_end(self):
        for p in self.points.values():
            p.calculate_distance_to_end()

