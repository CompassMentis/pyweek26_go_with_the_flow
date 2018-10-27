import pygame

from thing import Thing, Things
# from thing import desaturate
from vehicle import Vehicle


class Traveller(Thing):
    folder = 'images/travellers'

    def __init__(self, screen, name, x, y):
        super().__init__(screen, name, x, y)

        self.hotel = None
        self.plan = []

        # Current location, can be a hotel or a car
        self.location = None

        self.visited = []

    @property
    def done(self):
        # Visited everything on the plan, and back at the hotel
        return (not self.yet_to_visit) and self.location == self.hotel

    @property
    def yet_to_visit(self):
        return [d for d in self.plan if d not in self.visited]

    def show(self):
        self.screen.blit(
            self.image_desaturated if self.done else self.image,
            (self.x, self.y)
        )


class Travellers(Things):
    plan_x = 1375
    plan_y = 10
    plan_row_height = 48
    plan_column_width = 35
    plan_width = 150
    plan_hotel_x = 1530
    things_class = Traveller

    def show(self):
        for i, traveller in enumerate(self.things):
            if type(traveller.location) == Vehicle and traveller.location.retired:
                traveller.location = traveller.hotel
                traveller.visited = []

            traveller.x = self.plan_x
            traveller.y = self.plan_y + i * self.plan_row_height
            traveller.show()

            # Show hotel - desaturate if done
            hotel = traveller.hotel
            self.screen.blit(
                hotel.image_desaturated if traveller.done else hotel.image,
                (self.plan_hotel_x, traveller.y)
            )

            # Show destinations - desaturate if already visited
            for j, destination in enumerate(traveller.plan):
                x = self.plan_x + (j + 1) * self.plan_column_width
                self.screen.blit(
                    destination.plan_image_desaturated if destination in traveller.visited else destination.plan_image,
                    (x, traveller.y)
                )

            if type(traveller.location) == Vehicle:
                colour_name = traveller.location.colour_name
                colour = dict(
                    red=(255, 0, 0),
                    blue=(0, 0, 255),
                    yellow=(255, 255, 0)
                )[colour_name]
                active = traveller.location.active
                box_rect_relative = (traveller.x - 3, traveller.y - 3, self.plan_width - 2, self.plan_row_height - 5)
                box_rect_absolute = (
                    box_rect_relative[0],
                    box_rect_relative[1],
                    box_rect_relative[0] + box_rect_relative[2],
                    box_rect_relative[1] + box_rect_relative[3],
                )
                if active:
                    # Box around the traveller, in the car colour
                    # Yellow is too faint, so use a thicker line
                    pygame.draw.rect(self.screen, colour, box_rect_relative, 2 if colour_name == 'yellow' else 1)
                else:
                    # Box around the traveller, vertical lines in car colour, horizontal grey
                    pygame.draw.line(self.screen, colour,
                                     (box_rect_absolute[0], box_rect_absolute[1]),
                                     (box_rect_absolute[0], box_rect_absolute[3]),
                                     2)
                    pygame.draw.line(self.screen, colour,
                                     (box_rect_absolute[2], box_rect_absolute[1]),
                                     (box_rect_absolute[2], box_rect_absolute[3]),
                                     2)
                    pygame.draw.line(self.screen, (200, 200, 200),
                                     (box_rect_absolute[0], box_rect_absolute[1]),
                                     (box_rect_absolute[2], box_rect_absolute[1]),
                                     1)
                    pygame.draw.line(self.screen, (200, 200, 200),
                                     (box_rect_absolute[0], box_rect_absolute[3]),
                                     (box_rect_absolute[2], box_rect_absolute[3]),
                                     1)
