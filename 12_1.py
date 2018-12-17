import re

with open('inputs/day12_1.txt') as f:
    myInput = f.read().strip()


initialStateRegex = r"initial state: (.*)\n"

m = re.match(initialStateRegex, myInput)
initialState = [p for p in m.groups()[0]]

# save it as a dict instead (so that we can have negative keys)
initialState = {idx: p for (idx, p) in enumerate(initialState)}

# Add some room
for i in range(50):
    initialState[-1 * (i + 1)] = '.'
    initialState[max(initialState.keys()) + 1] = '.'

# Parse rules

ruleRegex = r"([\.|\#]{5}) => ([\.|\#])"
parsedRules = re.findall(ruleRegex, myInput)

alivePatterns = [r[0] for r in parsedRules if r[1] == '#']


def printState(state):
    print ''.join([state[key] for key in sorted(state.keys())])

# 20 generations
currentState = {key: value for (key, value) in initialState.items()}
for gen in range(50):
    newState = {}

    minPlant = min(
        [idx for (idx, value) in currentState.items() if value == '#'])
    maxPlant = max(
        [idx for (idx, value) in currentState.items() if value == '#'])

    for cellIdx in range(minPlant - 2, maxPlant + 2):
        neighborPattern = (
            currentState[cellIdx - 2] +
            currentState[cellIdx - 1] +
            currentState[cellIdx] +
            currentState[cellIdx + 1] +
            currentState[cellIdx + 2]
        )

        if neighborPattern in alivePatterns:
            newState[cellIdx] = '#'
        else:
            newState[cellIdx] = '.'
    # Fill other (edge) cells
    for cellIdx in [key for key in currentState.keys() if key not in newState.keys()]:
        newState[cellIdx] = '.'

    # printState(newState)
    print sum([key for (key, cell) in currentState.items() if cell == '#'])
    currentState = newState
