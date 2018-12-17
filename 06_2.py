from shared_geometry import Point, Vector, get_convex_hull

with open('inputs/day6_1.txt') as f:
    parsedInput = f.read().strip().split('\n')
SAFE_LIMIT = 10000


points = [Point(int(x.split(', ')[0]), int(x.split(', ')[1]))
          for x in parsedInput]

print points

x_left = min([p.x for p in points])
x_right = max([p.x for p in points])

y_high = min([p.y for p in points])
y_low = max([p.y for p in points])


def manhattan_distance(p1, p2):
    return abs(p2.y - p1.y) + abs(p2.x - p1.x)


def sum_distance_to_points(x, y):
    current_sum = 0
    for p in points:
        current_sum += manhattan_distance(p, Point(x, y))
    return current_sum


def get_nb_safe_points(around_distance):
    nb_of_safe_points = 0  # nb of points whose sum of distance is < SAFE_LIMIT
    for x in xrange(x_left - around_distance, x_right + around_distance):
        for y in xrange(y_high - around_distance, y_low + around_distance):
            is_safe = sum_distance_to_points(x, y) < SAFE_LIMIT
            nb_of_safe_points += 1 if is_safe else 0
    return nb_of_safe_points

zoom_out = 0
nb_safe_points = 0


has_changed = True
while has_changed:
    has_changed = False
    print "=====", zoom_out
    new_nb_safe_points = get_nb_safe_points(zoom_out)
    if (new_nb_safe_points != nb_safe_points):
        has_changed = True

    print new_nb_safe_points
    nb_safe_points = new_nb_safe_points
    zoom_out += 100
    print has_changed

print nb_safe_points
