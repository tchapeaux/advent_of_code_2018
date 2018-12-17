import math


def distance(p1, p2):
    dy = p2.y - p1.y
    dx = p2.x - p1.x
    return math.sqrt(dy * dy + dx * dx)


def get_convex_hull(points):
    convex_hull = []
    # First point is the one with the smallest x (arbitrarily)
    # Equality is not an issue
    smallest_x = None
    first_point = sorted([(p.x, p) for p in points])[0][1]
    convex_hull.append(first_point)

    current_point = first_point
    while len(convex_hull) == 1 or current_point != first_point:
        # Find next point in Convex Hull
        # The next point is the point such that every other point is
        # left of it
        next_point = None
        other_points = [p for p in points if p is not current_point]
        for p in other_points:
            if (next_point is None):
                v1 = Vector(current_point, p)
                for p2 in [_p for _p in other_points if _p is not p]:
                    v2 = Vector(p, p2)
                    is_left = v1.isLeftTurn(v2)
                    if (not is_left):
                        break
                else:
                    next_point = p
        assert next_point is not None
        if (next_point is not first_point):
            convex_hull.append(next_point)
        current_point = next_point

    return convex_hull


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "P({0},{1})".format(self.x, self.y)


class Vector:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    @property
    def x(self):
        return self.p2.x - self.p1.x

    @property
    def y(self):
        return self.p2.y - self.p1.y

    def norm(self):
        return distance(self.p1, self.p2)

    def angleWith(self, v2):
        # Between -PI and PI
        angle = math.atan2(v2.y, v2.x) - math.atan2(self.y, self.x)
        if angle < -math.pi:
            angle += 2 * math.pi
        if angle > math.pi:
            angle -= 2 * math.pi

        return angle

    def crossProduct(self, v2):
        return self.norm() * v2.norm() * math.sin(self.angleWith(v2))

    def isLeftTurn(self, v2, strict=False):
        _sinAngle = math.sin(self.angleWith(v2))
        return _sinAngle > 0 if strict else _sinAngle >= 0

if __name__ == '__main__':
    p1 = Point(0, 0)
    p2 = Point(10, 10)
    p3 = Point(20, 0)

    print distance(p1, p2)

    v1 = Vector(p1, p2)
    v2 = Vector(p1, p3)

    print v1.angleWith(v2)

    print v1.isLeftTurn(v2)
    print v2.isLeftTurn(v1)
