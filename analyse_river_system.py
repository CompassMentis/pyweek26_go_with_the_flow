import os
import imageio
import math

from points import Points, START_VALUE, MIDDLE_VALUE, END_VALUE

# calculate angle from angle between the two points three steps either way
ANGLE_POINTS_DELTA = 3
ANGLE_POINTS = ANGLE_POINTS_DELTA * 2 + 1


def follow_line(image, points, x, y):
    print("Follow line, starting at ", start_point)
    points.add_point(x, y)

    first_point = True
    done = False
    while not done:
        for i, j in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            x2, y2 = x + i, y + j
            point_colour = list(image[x2, y2])

            # If it is a middle or end value, add it to the line and move to it
            if (point_colour == MIDDLE_VALUE and not points.contains(x2, y2)) or \
                    (point_colour == END_VALUE and not first_point):
                points.add_point(x2, y2)
                x, y = x2, y2
                first_point = False
                if point_colour == END_VALUE:
                    done = True
                break
        else:
            print(f'Stuck at {x}, {y}')
    print("Stopped at ", x, y)
    points.next_segment()


def calculate_angle(point_a, point_b):
    # Calculate the angle going from point_a to point_b, relative to north
    delta_x = point_b.x - point_a.x
    delta_y = point_b.y - point_a.y
    angle = math.atan2(delta_y, delta_x)
    return int(math.degrees(angle))


def calculate_angles_for_segment(start_point):
    segment_points = []
    p = start_point
    while p is not None:
        segment_points.append(p)
        p = p.next

    if len(segment_points) < ANGLE_POINTS:
        angle = calculate_angle(segment_points[0], segment_points[-1])
        for p in segment_points:
            p.angle = angle
        return

    # First ANGLE_POINTS_DELTA + 1, use angle from (ANGLE_POINTS_DELTA + 1)th point
    angle = calculate_angle(segment_points[0], segment_points[ANGLE_POINTS - 1])
    for i in range(ANGLE_POINTS_DELTA):
        segment_points[i].angle = angle

    # Ditto for last ANGLE_POINTS_DELTA + 1, but from the end
    angle = calculate_angle(segment_points[-ANGLE_POINTS], segment_points[-1])
    for i in range(ANGLE_POINTS_DELTA + 1):
        segment_points[-i].angle = angle

    for i in range(ANGLE_POINTS_DELTA, len(segment_points) - ANGLE_POINTS_DELTA):
        segment_points[i].angle = calculate_angle(segment_points[i - ANGLE_POINTS_DELTA], segment_points[i + ANGLE_POINTS_DELTA])


image = imageio.imread(os.path.join('images', 'river_system.png'))

# Todo: Use numpy functionality to speed this up
start_points = []
for i in range(image.shape[0]):
    if i % 100 == 0:
        print(i)
    for j in range(image.shape[1]):
        pixel = list(image[i, j])
        if pixel == START_VALUE:
            start_points.append((i, j))

points = Points()
for start_point in start_points:
    follow_line(image, points, start_point[0], start_point[1])

points.link_segments(image)
points.calculate_distances_to_end()

for start_point in start_points:
    calculate_angles_for_segment(points.points[start_point])

print("Writing data to file")
with open('river_system.txt', 'w') as output_file:
    points.write(output_file)
