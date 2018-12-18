from itertools import product
from copy import deepcopy

with open('inputs/day18_1.txt') as f:
    myInput = f.read().split('\n')

myInput = [_.strip() for _ in myInput if len(_.strip()) > 0]


class TerrainEnum:
    OPEN = '.'
    TREES = '|'
    LUMBER = '#'

terrain = []
for y, row in enumerate(myInput):
    terrain.append([])
    for x, cell in enumerate(row):
        terrain[y].append(cell)


def printTerrain():
    _s = ''
    for y, row in enumerate(terrain):
        for x, cell in enumerate(row):
            _s += cell
        _s += '\n'
    print _s


def getNeighbors(x, y):
    y_range = [y]
    x_range = [x]
    if y > 0:
        y_range.append(y - 1)
    if y < len(terrain) - 1:
        y_range.append(y + 1)
    if x > 0:
        x_range.append(x - 1)
    if x < len(terrain[y]) - 1:
        x_range.append(x + 1)

    neighbors = []
    for (_x, _y) in product(x_range, y_range):
        if _x == x and _y == y:
            # skip x, y itself
            continue
        neighbors.append(terrain[_y][_x])
    return neighbors

print "Initial state"
printTerrain()

tick = 0
while tick < 1000:
    newTerrain = deepcopy(terrain)

    for y, row in enumerate(terrain):
        for x, cell in enumerate(row):
            neighbors = getNeighbors(x, y)
            openNeighbors = [n for n in neighbors if n == TerrainEnum.OPEN]
            treesNeighbors = [n for n in neighbors if n == TerrainEnum.TREES]
            lumberNeighbors = [n for n in neighbors if n == TerrainEnum.LUMBER]

            # DEBUG
            """
            if y == 5 and x == 4:
                print x, y, cell
                print neighbors
            """

            if cell == TerrainEnum.OPEN:
                if len(treesNeighbors) >= 3:
                    newTerrain[y][x] = TerrainEnum.TREES
            elif cell == TerrainEnum.TREES:
                if len(lumberNeighbors) >= 3:
                    newTerrain[y][x] = TerrainEnum.LUMBER
            else:
                assert cell == TerrainEnum.LUMBER
                if len(lumberNeighbors) == 0 or len(treesNeighbors) == 0:
                    newTerrain[y][x] = TerrainEnum.OPEN

    terrain = newTerrain
    tick += 1
    print "tick", tick
    printTerrain()

nbTrees = sum([sum([1 for cell in row if cell == TerrainEnum.TREES])
               for row in terrain])
nbLumber = sum([sum([1 for cell in row if cell == TerrainEnum.LUMBER])
                for row in terrain])

print "Total resource value", nbTrees, 'x', nbLumber, nbTrees * nbLumber
