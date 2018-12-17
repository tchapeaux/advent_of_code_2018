# Parse input
INPUT_PATH = "inputs/day8_1.txt"
with open(INPUT_PATH) as f:
    parsedInput = f.read().strip().split(' ')

inputArray = parsedInput
curIdx = 0


def readNode():
    global curIdx
    nbChild = int(inputArray[curIdx])
    curIdx += 1
    nbMeta = int(inputArray[curIdx])
    node = {"children": [], "meta": []}

    for _c in range(nbChild):
        curIdx += 1
        child = readNode()  # this will increment curIdx
        node["children"].append(child)

    for _m in range(nbMeta):
        curIdx += 1
        node["meta"].append(int(inputArray[curIdx]))

    return node

root = readNode()


def printNode(node, tabLevel=0):
    print "\t" * tabLevel, "NODE"
    for child in node["children"]:
        printNode(child, tabLevel + 1)
    for meta in node["meta"]:
        print "\t" * tabLevel, meta

printNode(root)


def getNodeValue(node):
    # Dynamic programming
    # Always store the value of a node inside it (node["value"]) before returning
    # So that we can reuse past results

    if "value" not in node:
        hasChild = len(node["children"]) > 0

        if not hasChild:
            node["value"] = sum(node["meta"])
        else:
            currentSum = 0
            for meta in node["meta"]:
                if meta > 0 and meta <= len(node["children"]):
                    currentSum += getNodeValue(node["children"][meta - 1])
            node["value"] = currentSum

    return node["value"]

print "root value is"
print getNodeValue(root)
