import Queue
import pdb

terrain = []  # terrain[y][x] = square at X, Y
elves = []
goblins = []


def getSquare(x, y):
    return terrain[y][x]


def getNeighbors(x, y):
    # Return them in reading order
    return [
        (x, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x, y + 1),
    ]


def isFreeSquare(x, y):
    return getSquare(x, y) == TerrainEnum.FREE and not any([
        u.x == x and u.y == y for u in elves + goblins if not u.dead
    ])


class TerrainEnum:
    WALL = '#'
    FREE = '.'
    GOBLIN = 'G'
    ELF = 'E'


class Unit(object):

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.hitpoints = 200
        self.strength = self.STRENGTH

    @property
    def dead(self):
        return self.hitpoints <= 0

    def enemyInRange(self):
        neighbors = getNeighbors(self.x, self.y)
        return any([
            (e.x, e.y) in neighbors
            for e in self.enemies
            if not e.dead
        ])

    def move(self):
        if self.enemyInRange():
            if VERBOSE:
                print self.name, "does not move (enemy in range)"
            return

        targets = [t for t in self.enemies if not t.dead]
        squaresToGo = set()
        for t in sorted(targets, readingOrder):
            for (x, y) in getNeighbors(t.x, t.y):
                if isFreeSquare(x, y):
                    squaresToGo.add((x, y))

        curShortestDist = 200
        equallyShortestPaths = []
        # Sort square by manhattan distance in the hope of optimizing (does not
        # work well)
        for s in sorted(squaresToGo, manhattanDistanceTo(self)):
            shortPath = getShortestPath(self.x, self.y, s[0], s[
                                        1], maxDist=curShortestDist)
            if shortPath is None:
                continue

            if shortPath.dist == curShortestDist:
                equallyShortestPaths.append(shortPath)
            elif shortPath.dist < curShortestDist:
                equallyShortestPaths = [shortPath]
                curShortestDist = shortPath.dist

        if len(equallyShortestPaths) == 0:
            if VERBOSE:
                print self.name, "does not move (nowhere to move)"
            return
        firstShortestPath = sorted(equallyShortestPaths, readingOrder)[0]
        firstSquare = firstShortestPath.firstStep()
        assert abs(firstSquare.y - self.y + firstSquare.x - self.x) == 1
        self.x = firstSquare.x
        self.y = firstSquare.y
        if VERBOSE:
            print self.name, "moves to", self.x, self.y

    def attack(self):
        neighbors = getNeighbors(self.x, self.y)
        targets = [
            e for e in self.enemies
            if (e.x, e.y) in neighbors and not e.dead
        ]
        if len(targets) == 0:
            if VERBOSE:
                print self.name, "does not attack (no target)"
            return
        # Sort in reading order then take first target with minimal HP
        minHitpoints = min([t.hitpoints for t in targets])
        target = sorted(
            [t for t in targets if t.hitpoints == minHitpoints],
            readingOrder
        )[0]

        target.hitpoints -= self.strength
        if target.dead and isinstance(target, Elf):
            raise ElfDeath()
        if VERBOSE:
            print self.name, "attacks", target.name, "(remaining=", target.hitpoints, ')'
            if target.dead:
                print target.name, "dies"


class Goblin(Unit):
    enemies = elves
    enemyType = TerrainEnum.ELF
    STRENGTH = 3


class Elf(Unit):
    enemies = goblins
    enemyType = TerrainEnum.GOBLIN
    STRENGTH = 3


class ElfDeath(Exception):
    pass


def readingOrder(unit1, unit2):
    dy = unit1.y - unit2.y
    if dy == 0:
        return unit1.x - unit2.x
    return dy


def manhattanDistance(x1, y1, x2, y2):
    return abs(y2 - y1) + abs(x2 - x1)


def manhattanDistanceTo(unit):
    # Used for sorting based on a unit
    def _dist(xy1, xy2):
        d1 = manhattanDistance(unit.x, unit.y, xy1[0], xy1[1])
        d2 = manhattanDistance(unit.x, unit.y, xy2[0], xy2[1])
        return d1 - d2

    return _dist


class PathNode:

    def __init__(self, x, y, dist, prev):
        self.x = x
        self.y = y
        self.dist = dist
        self.prev = prev

    def firstStep(self):
        cur = self
        while cur.dist > 1:
            cur = cur.prev
        return cur

    def __repr__(self):
        _s = 'path('
        cur = self
        while cur.prev:
            _s += '(' + str(cur.x) + ',' + str(cur.y) + '), '
            cur = cur.prev
        return _s


def getShortestPath(x1, y1, x2, y2, maxDist=None):
    nodesToVisit = Queue.Queue()
    nodesToVisit.put(PathNode(x1, y1, 0, None))
    alreadyVisited = set()
    alreadyAdded = set()
    while not nodesToVisit.empty() > 0:
        newNode = nodesToVisit.get()
        if (newNode in alreadyVisited):
            continue
        alreadyVisited.add((newNode.x, newNode.y))

        if maxDist and newNode.dist > maxDist:
            # Give up
            return None

        # print len(alreadyVisited), nodesToVisit.qsize(), x1, y1, x2, y2

        # Check out neighbors
        for n in getNeighbors(newNode.x, newNode.y):
            neighborNode = PathNode(n[0], n[1], newNode.dist + 1, newNode)

            # If we have reached node 2, return
            # (I'm assuming that because we go through neighbor in reading order,
            # and we're using a queue, we will always find the shortest path
            # first)
            if neighborNode.x == x2 and neighborNode.y == y2:
                # print "found", x1, y1, x2, y2, "in", neighborNode.dist
                return neighborNode

            # Otherwise, add it to the stack to visit
            x, y = neighborNode.x, neighborNode.y
            # pdb.set_trace()
            isFree = isFreeSquare(x, y)
            isNew = (x, y) not in alreadyAdded
            if isFree and isNew:
                nodesToVisit.put(neighborNode)
                alreadyAdded.add((x, y))

    return None


def printTerrain():
    _s = ''
    for y, row in enumerate(terrain):
        elvesHere = [e for e in elves if e.y == y and not e.dead]
        goblinsHere = [g for g in goblins if g.y == y and not g.dead]
        for x, square in enumerate(row):
            if any([e.x == x for e in elvesHere]):
                _s += TerrainEnum.ELF
            elif any([g.x == x for g in goblinsHere]):
                _s += TerrainEnum.GOBLIN
            else:
                _s += square
        if len(elvesHere + goblinsHere) > 0:
            _s += '\t'
            _s += '\t'.join([g.name + '(' + str(g.hitpoints) +
                             ')' for g in goblinsHere])
            _s += '\t' if len(goblinsHere) > 0 else ''
            _s += '\t'.join([e.name +
                             '(' + str(e.hitpoints) + ')' for e in elvesHere])
        _s += '\n'
    print(_s)


def runSimulation(inputPath):
    global terrain
    global elves
    global goblins

    with open(inputPath) as f:
        myInput = f.read().strip()

    Elf.STRENGTH = 3
    ELVES_NOT_POWERFUL_ENOUGH = True
    while ELVES_NOT_POWERFUL_ENOUGH:
        print "TRYING with strength", Elf.STRENGTH
        del terrain[:]
        del elves[:]
        del goblins[:]

        for y, row in enumerate(myInput.split('\n')):
            row = row.strip()
            terrain.append([])
            for x, square in enumerate(row):
                if square == TerrainEnum.GOBLIN:
                    goblins.append(Goblin('gob ' + str(len(goblins)), x, y))
                    terrain[y].append(TerrainEnum.FREE)
                elif square == TerrainEnum.ELF:
                    elves.append(Elf('elf ' + str(len(elves)), x, y))
                    terrain[y].append(TerrainEnum.FREE)
                else:
                    terrain[y].append(square)

        try:
            _round = 0
            if VERBOSE:
                print "round", _round
                printTerrain()

            RUNNING = True
            while RUNNING:
                for unit in sorted(elves + goblins, readingOrder):
                    if unit.dead:
                        continue

                    aliveEnemies = [e for e in unit.enemies if not e.dead]
                    if len(aliveEnemies) == 0:
                        RUNNING = False
                        break

                    unit.move()
                    unit.attack()

                if RUNNING:
                    _round += 1
                    # print "round", _round
                    # printTerrain()

            print "Elves are all alives!"

            remainingHitPoints = sum(
                [u.hitpoints for u in elves + goblins if not u.dead])
            checksum = _round * remainingHitPoints
            print "=>", _round, '*', remainingHitPoints, '=', checksum
            return checksum

        except ElfDeath:
            Elf.STRENGTH += 1
        except:
            raise

VERBOSE = False

assert runSimulation('inputs/day15_example_1.txt') == 4988
assert runSimulation('inputs/day15_example_3.txt') == 31284
assert runSimulation('inputs/day15_example_4.txt') == 3478
assert runSimulation('inputs/day15_example_5.txt') == 6474
assert runSimulation('inputs/day15_example_6.txt') == 1140

print runSimulation("inputs/day15_1.txt")
