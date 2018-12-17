from PIL import Image, ImageDraw
from collections import deque

with open('inputs/day17_1.txt')as f:
    myInput = f.read().split('\n')

myInput = [row.strip() for row in myInput if len(row.strip()) > 0]
myInput = [(row.split(', ')[0], row.split(', ')[1]) for row in myInput]

# Generate coords from input

cells = []
for cell_descr in myInput:
    (coord1, coord2) = cell_descr
    if coord1.startswith('x'):
        x_coord = coord1[2:]
        y_coord = coord2[2:]
        [y_min, y_max] = y_coord.split('..')
        for y in range(int(y_min), int(y_max) + 1):
            cells.append((int(x_coord), y))
    else:
        assert coord1.startswith('y')
        x_coord = coord2[2:]
        y_coord = coord1[2:]
        [x_min, x_max] = x_coord.split('..')
        for x in range(int(x_min), int(x_max) + 1):
            cells.append((x, int(y_coord)))


class GroundType:
    SAND = '.'
    CLAY = '#'
    SETTLED_WATER = '~'
    FLOWING_WATER = '|'

ground = {}  # shallow matrix


def getCell(x, y):
    if x == 500 and y == 0:
        return '+'
    if x not in ground or y not in ground[x]:
        return GroundType.SAND
    return ground[x][y]


def setCell(x, y, val):
    if x not in ground:
        ground[x] = {}
    ground[x][y] = val


def isSolid(x, y):
    val = getCell(x, y)
    return val == GroundType.CLAY or val == GroundType.SETTLED_WATER


for (cell_x, cell_y) in cells:
    setCell(cell_x, cell_y, GroundType.CLAY)

# Bounding box borders
min_x = min([x for x in ground.keys()])
max_x = max([x for x in ground.keys()])
min_y = min([
    min([y for y in ground[x].keys()])
    for x in ground.keys()
])
max_y = max([
    max([y for y in ground[x].keys()])
    for x in ground.keys()
])


IMG_NAME_IDX = 0


def printGround():
    global IMG_NAME_IDX

    img = Image.new('RGB', (max_x - min_x + 10,
                            max_y - min_y + 10),  "black")
    draw = ImageDraw.Draw(img)
    _s = ''
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            val = getCell(x, y)
            if val == GroundType.CLAY:
                draw.point((x - min_x, y - min_y), "grey")
            if val == GroundType.SETTLED_WATER:
                draw.point((x - min_x, y - min_y), (100, 100, 255))
            if val == GroundType.FLOWING_WATER:
                draw.point((x - min_x, y - min_y), "white")
            _s += val
        _s += '\n'
    # print _s
    img.save('17_out_' + str(IMG_NAME_IDX) + '.png')
    IMG_NAME_IDX += 1
    if max_x <= 500 + 80:
        print _s

print "Initial state"
printGround()

# Simulate until stabilization
settledWaterCount = 0
sources = deque([(500, 0)])
iter_count = 0
while len(sources) > 0:
    iter_count += 1
    offscreen = False

    if iter_count % 10000 == 0:
        print "where am I?"
        printGround()
    if iter_count % 100000 == 0:
        print "I'm bored"
        break

    (s_x, s_y) = sources.popleft()
    print "source", (s_x, s_y)

    if getCell(s_x, s_y) == GroundType.SETTLED_WATER:
        continue

    setCell(s_x, s_y, GroundType.FLOWING_WATER)

    # water falls
    off_y = 0
    while not isSolid(s_x, s_y + off_y + 1):
        off_y += 1
        setCell(s_x, s_y + off_y, GroundType.FLOWING_WATER)
        if off_y + 1 > max_y:
            offscreen = True
            break
    print "\tfalls", off_y, "until", s_x, s_y + off_y

    if offscreen:
        continue

    # Inspect left
    off_x_left = 0
    left_wall = False
    # water moves left until a wall or a hole is encountered
    while not isSolid(s_x - off_x_left - 1, s_y + off_y) and isSolid(s_x - off_x_left, s_y + off_y + 1):
        off_x_left += 1
        setCell(s_x - off_x_left, s_y + off_y, GroundType.FLOWING_WATER)
    print "\tslides left", off_x_left, "until", s_x - off_x_left, s_y + off_y

    left_wall = isSolid(s_x - off_x_left - 1, s_y +
                        off_y) and isSolid(s_x - off_x_left, s_y + off_y + 1)
    print "\thas left_wall?", left_wall
    if not isSolid(s_x - off_x_left, s_y + off_y + 1):
        sources.append((s_x - off_x_left, s_y + off_y))

    # Inspect right
    off_x_right = 0
    right_wall = False
    # water moves right until a wall or a hole is encountered
    while not isSolid(s_x + off_x_right + 1, s_y + off_y) and isSolid(s_x + off_x_right, s_y + off_y + 1):
        off_x_right += 1
        setCell(s_x + off_x_right, s_y + off_y, GroundType.FLOWING_WATER)
    print "\tslides right", off_x_right, "until", s_x + off_x_right, s_y + off_y

    right_wall = isSolid(s_x + off_x_right + 1, s_y +
                         off_y) and isSolid(s_x + off_x_right, s_y + off_y + 1)
    print "\thas right_wall?", right_wall
    if not isSolid(s_x + off_x_right, s_y + off_y + 1):
        sources.append((s_x + off_x_right, s_y + off_y))

    # If there is a wall on each side, water is settled
    if left_wall and right_wall:
        for off_x in range(-1 * off_x_left, off_x_right + 1):
            setCell(s_x + off_x, s_y + off_y, GroundType.SETTLED_WATER)

        # Add a source just above the point of contact
        sources.append((s_x, s_y + off_y - 1))

    # printGround()

print "final state"
printGround()

# Count water
waterCnt = 0
for (x, row) in ground.items():
    for (y, cell) in row.items():
        if y >= min_y and y <= max_y:
            if cell in [GroundType.SETTLED_WATER, GroundType.FLOWING_WATER]:
                waterCnt += 1
print "water count", waterCnt

# too low: 39139
# I see that I'm missing 25 cells because of some bug...
# too high: 39164 (oops)
# maybe it's a OBO...
# too high: 39163 (erk no)
# oh wait I counted some where y < min_y...
# 39162 (OK)

# PART 2

# Count settled water
settledWaterCnt = 0
for (x, row) in ground.items():
    for (y, cell) in row.items():
        if y >= min_y and y <= max_y:
            if cell in [GroundType.SETTLED_WATER]:
                settledWaterCnt += 1
print "settled water count", settledWaterCnt
