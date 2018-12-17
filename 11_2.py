from itertools import product


def getPowerLevel(x, y, serialNb):
    rackId = x + 10
    powerLevelStart = rackId * y
    _value = powerLevelStart + serialNb
    _value *= rackId
    _value = str(_value)[-3] if len(str(_value)) > 2 else 0
    return int(_value) - 5

# assert getPowerLevel(3, 5, 8) == 4
# assert getPowerLevel(122, 79, 57) == -5.
# assert getPowerLevel(217, 196, 39) == 0.
# assert getPowerLevel(101, 153, 71) == 4.

# Construct GRID

serialNb = 6303
grid = []
for _x in range(300):
    grid.append([])
    for _y in range(300):
        grid[_x].append(getPowerLevel(_x + 1, _y + 1, serialNb))

# Scan for biggest square

currentMax = -100000
currentCoord = None
for _size in range(300):
    print(currentCoord[0] + 1, currentCoord[1] + 1,
          currentCoord[2]) if currentCoord is not None else '/'
    for _x in range(300 - _size + 1):
        prevSum = None
        for _y in range(300 - _size + 1):
            if prevSum is None:
                mySum = sum([
                    grid[_xx][_yy]
                    for (_xx, _yy)
                    in product(range(_x, _x + _size), range(_y, _y + _size))
                ])
            else:
                # remove top row at _y - 1
                mySum = prevSum - sum([grid[_xx][_y - 1]
                                       for _xx in range(_x, _x + _size)])
                # add bottom row at _y + _size - 1
                mySum += sum([grid[_xx][_y + _size - 1]
                              for _xx in range(_x, _x + _size)])

            if mySum > currentMax:
                currentMax = mySum
                currentCoord = (_x, _y, _size)

            prevSum = mySum
    print "SIZE", _size

print currentMax
print currentCoord[0] + 1, currentCoord[1] + 1, currentCoord[2]
