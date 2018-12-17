from shared_geometry import Point, Vector, get_convex_hull

with open('inputs/day6_1.txt') as f:
    parsedInput = f.read().strip().split('\n')

points = [Point(int(x.split(', ')[0]), int(x.split(', ')[1]))
          for x in parsedInput]

print points

x_left = min([p.x for p in points])
x_right = max([p.x for p in points])

y_high = min([p.y for p in points])
y_low = max([p.y for p in points])

# Compute convex hull
# My hypothesis is that only points from the convex hull will have an
# infinite area
convex_hull = get_convex_hull(points)
non_convex_hull_points = [p for p in points if p not in convex_hull]


print "quick recap"
print "ZONE l t r b", x_left, y_high, x_right, y_low
print "len points", len(points)
print "len convex hull", len(convex_hull)
print "len others", len(non_convex_hull_points)


def manhattan_distance(p1, p2):
    return abs(p2.y - p1.y) + abs(p2.x - p1.x)


def closest_point(x, y):
    current_point = None
    current_distance = -1
    for p in points:
        dist = manhattan_distance(p, Point(x, y))
        if dist == current_distance:
            # Special case - equidistant point - invalidate the result
            current_point = None
        if current_distance == -1 or dist < current_distance:
            current_distance = dist
            current_point = p

    return current_point


def closest_point_map(around_distance):
    _map = {}
    for x in xrange(x_left - around_distance, x_right + around_distance):
        for y in xrange(y_high - around_distance, y_low + around_distance):
            _closest_point = closest_point(x, y)
            if _closest_point not in _map:
                _map[_closest_point] = 0
            _map[_closest_point] += 1
    return _map

zoom_out = 0
voronoi_size = {p: 0 for p in non_convex_hull_points}

has_changed = True
while has_changed:
    has_changed = False
    print "=====", zoom_out
    new_voronoi_size = closest_point_map(zoom_out)

    print new_voronoi_size
    voronoi_size = new_voronoi_size
    zoom_out += 100

print voronoi_size
print max([(size, point) for (point, size) in voronoi_size.items()])
