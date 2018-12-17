import re
import os
import time

# Constants / Structure definitions

UP = 'UP'
RIGHT = 'RIGHT'
DOWN = 'DOWN'
LEFT = 'LEFT'

CLOCKWISE = [UP, RIGHT, DOWN, LEFT]
COUNTER_CLOCKWISE = [UP, LEFT, DOWN, RIGHT]

TURN_LEFT = 'TURN_LEFT'
GO_STRAIGHT = 'GO_STRAIGHT'
TURN_RIGHT = 'TURN_RIGHT'


def turnRight(direction):
    C = CLOCKWISE
    return C[(C.index(direction) + 1) % len(C)]

assert turnRight(UP) == RIGHT
assert turnRight(LEFT) == UP


def turnLeft(direction):
    C = COUNTER_CLOCKWISE
    return C[(C.index(direction) + 1) % len(C)]

assert turnLeft(UP) == LEFT
assert turnLeft(RIGHT) == UP

VERTICAL = 'VERTICAL'
HORIZONTAL = 'HORIZONTAL'
INTERSECTION = 'INTERSECTION'
ANGLE_TOPLEFT = 'ANGLE_TOPLEFT'
ANGLE_TOPRIGHT = 'ANGLE_TOPRIGHT'
ANGLE_BOTTOMLEFT = 'ANGLE_BOTTOMLEFT'
ANGLE_BOTTOMRIGHT = 'ANGLE_BOTTOMRIGHT'


class Cart:

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.nextTurn = TURN_LEFT
        self.dead = False


def cartOrder(c1, c2):
    # Used to sort cart in the specific order
    if c1.y - c2.y != 0:
        return c1.y - c2.y
    return c1.x - c2.x

railMap = []
carts = []

with open('inputs/day13_1.txt') as f:
    myInput = f.read().rstrip().split('\n')
for y, row in enumerate(myInput):
    railMap.append({})
    for x, cell in enumerate(row):
        if cell == '-':
            railMap[y][x] = HORIZONTAL
        elif cell == '|':
            railMap[y][x] = VERTICAL
        elif cell == '+':
            railMap[y][x] = INTERSECTION
        elif cell == '/':
            # Either ANGLE_TOPLEFT or ANGLE_BOTTOMRIGHT
            # Depending on the left tile
            if x == 0 or (x - 1) not in railMap[y] or railMap[y][x - 1] in [VERTICAL, ANGLE_TOPRIGHT, ANGLE_BOTTOMRIGHT]:
                railMap[y][x] = ANGLE_TOPLEFT
            else:
                railMap[y][x] = ANGLE_BOTTOMRIGHT
        elif cell == '\\':
            # Either ANGLE_TOPRIGHT or ANGLE_BOTTOMLEFT
            # Depending on the left tile
            if x == 0 or (x - 1) not in railMap[y] or railMap[y][x - 1] in [VERTICAL, ANGLE_BOTTOMRIGHT, ANGLE_TOPRIGHT]:
                railMap[y][x] = ANGLE_BOTTOMLEFT
            else:
                railMap[y][x] = ANGLE_TOPRIGHT
        elif cell == '<':
            railMap[y][x] = HORIZONTAL
            carts.append(Cart(x, y, LEFT))
        elif cell == '>':
            railMap[y][x] = HORIZONTAL
            carts.append(Cart(x, y, RIGHT))
        elif cell == '^':
            railMap[y][x] = VERTICAL
            carts.append(Cart(x, y, UP))
        elif cell == 'v':
            railMap[y][x] = VERTICAL
            carts.append(Cart(x, y, DOWN))
        elif cell != ' ' and cell != '\r':
            raise Exception('Unexpected symbol ' + cell)


def printMap():
    max_y = len(railMap)
    max_x = max([max(railMap[y].keys()) for y in range(len(railMap))])
    _mapStr = ''
    for y in range(max_y):
        for x in range(max_x + 1):
            if x not in railMap[y]:
                _mapStr += ' '
            else:
                cell = railMap[y][x]
                cartsHere = [
                    c for c in carts
                    if c.x == x and c.y == y and not c.dead
                ]
                if len(cartsHere) >= 2:
                    _mapStr += 'X'
                elif len(cartsHere) == 1:
                    cart = cartsHere[0]
                    if cart.direction == LEFT:
                        _mapStr += '<'
                    elif cart.direction == RIGHT:
                        _mapStr += '>'
                    elif cart.direction == UP:
                        _mapStr += '^'
                    elif cart.direction == DOWN:
                        _mapStr += 'v'
                else:
                    if cell == HORIZONTAL:
                        _mapStr += '-'
                    elif cell == VERTICAL:
                        _mapStr += '|'
                    elif cell == INTERSECTION:
                        _mapStr += '+'
                    elif cell == ANGLE_TOPRIGHT or cell == ANGLE_BOTTOMLEFT:
                        _mapStr += '\\'
                    elif cell == ANGLE_TOPLEFT or cell == ANGLE_BOTTOMRIGHT:
                        _mapStr += '/'

        _mapStr += '\n'
    print _mapStr

HAS_COLLISION = False
collisionAt = (-1, -1)
tick = 0
# print "tick 0"
# printMap()
while len([c for c in carts if not c.dead]) > 1:
    tick += 1

    for cart in sorted(carts, cartOrder):
        # If already collided, do not move
        if cart.dead:
            continue

        if cart.direction == UP:
            cart.y -= 1
            if railMap[cart.y][cart.x] == ANGLE_TOPRIGHT:
                cart.direction = LEFT
            elif railMap[cart.y][cart.x] == ANGLE_TOPLEFT:
                cart.direction = RIGHT
        elif cart.direction == DOWN:
            cart.y += 1
            if railMap[cart.y][cart.x] == ANGLE_BOTTOMRIGHT:
                cart.direction = LEFT
            elif railMap[cart.y][cart.x] == ANGLE_BOTTOMLEFT:
                cart.direction = RIGHT
        elif cart.direction == LEFT:
            cart.x -= 1
            if railMap[cart.y][cart.x] == ANGLE_TOPLEFT:
                cart.direction = DOWN
            elif railMap[cart.y][cart.x] == ANGLE_BOTTOMLEFT:
                cart.direction = UP
        elif cart.direction == RIGHT:
            cart.x += 1
            if railMap[cart.y][cart.x] == ANGLE_TOPRIGHT:
                cart.direction = DOWN
            elif railMap[cart.y][cart.x] == ANGLE_BOTTOMRIGHT:
                cart.direction = UP

        # Intersection: change direction and increment state
        if railMap[cart.y][cart.x] == INTERSECTION:
            if cart.nextTurn == TURN_LEFT:
                cart.direction = turnLeft(cart.direction)
                cart.nextTurn = GO_STRAIGHT
            elif cart.nextTurn == GO_STRAIGHT:
                cart.nextTurn = TURN_RIGHT
            elif cart.nextTurn == TURN_RIGHT:
                cart.direction = turnRight(cart.direction)
                cart.nextTurn = TURN_LEFT

        # Check for collisions
        for _otherCart in [c for c in carts if c != cart and not c.dead]:
            if _otherCart.x == cart.x and _otherCart.y == cart.y:
                cart.dead = True
                _otherCart.dead = True

    # Console animation
    # Remove for performance or on Windows
    if len(railMap) < 100:
        # time.sleep(0.03)
        # os.system('clear')
        print "tick", tick
        printMap()

print "last tick", tick
printMap()

remainingCart = [c for c in carts if not c.dead][0]
print "Remaining cart at", remainingCart.x, remainingCart.y
