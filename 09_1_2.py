class Node:

    def __init__(self, value):
        self.value = value
        self.leftNode = None
        self.rightNode = None


class Wheel:

    def __init__(self):
        self.currentNode = Node(0)
        self.currentNode.leftNode = self.currentNode
        self.currentNode.rightNode = self.currentNode

    def addMarble(self, marbleValue):
        rightNode = self.currentNode.rightNode
        # construct new node
        newNode = Node(marbleValue)
        newNode.leftNode = rightNode
        newNode.rightNode = rightNode.rightNode
        # link new node to wheel
        newNode.rightNode.leftNode = newNode
        newNode.leftNode.rightNode = newNode

        self.currentNode = newNode

    def popMarble(self):
        _node = self.currentNode
        for _ in range(7):
            _node = _node.leftNode

        # Remove node from wheen
        _node.leftNode.rightNode = _node.rightNode
        _node.rightNode.leftNode = _node.leftNode

        self.currentNode = _node.rightNode
        return _node.value


def getMaxScore(NB_OF_ELVES, NB_OF_MARBLES):
    elvesScores = [0 for _ in range(NB_OF_ELVES)]

    wheel = Wheel()

    curMarble = 0

    while curMarble <= NB_OF_MARBLES - 23:
        # Place 22 previous marbles
        for i in range(22):
            curMarble += 1
            wheel.addMarble(curMarble)

        # Place the last marble and give score to player
        curMarble += 1
        curPlayer = curMarble % NB_OF_ELVES
        assert curMarble % 23 == 0
        elvesScores[curPlayer] += curMarble
        removedMarble = wheel.popMarble()
        elvesScores[curPlayer] += removedMarble

    return max(elvesScores)

# Examples
assert getMaxScore(9, 25) == 32
assert getMaxScore(10, 1618) == 8317
assert getMaxScore(13, 7999) == 146373
assert getMaxScore(17, 1104) == 2764
assert getMaxScore(21, 6111) == 54718
assert getMaxScore(30, 5807) == 37305

# 9_1
print "9_1", getMaxScore(441, 71032)

# 9_2
print "9_2", getMaxScore(441, 7103200)
