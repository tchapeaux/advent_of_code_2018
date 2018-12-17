import re

FIVE_DEAD = ['.', '.', '.', '.', '.']

with open('inputs/day12_1.txt') as f:
    myInput = f.read().strip()


initialStateRegex = r"initial state: (.*)\n"

m = re.match(initialStateRegex, myInput)
initialState = [p for p in m.groups()[0]]

# save it as a dict instead (so that we can have negative keys)
initialState = FIVE_DEAD + [p for p in initialState] + FIVE_DEAD
CURRENT_ZERO = 5


# Parse rules

ruleRegex = r"([\.|\#]{5}) => ([\.|\#])"
parsedRules = re.findall(ruleRegex, myInput)

alivePatterns = [r[0] for r in parsedRules if r[1] == '#']


def newGen(state):
    global CURRENT_ZERO
    newState = ['.' for _ in xrange(len(state))]

    for idx in xrange(2, len(newState) - 2):
        neighborPattern = (
            (state[idx - 2] if idx - 2 >= 0 else '.') +
            (state[idx - 1] if idx - 1 >= 0 else '.') +
            state[idx] +
            (state[idx + 1] if idx + 1 < len(state) else '.') +
            (state[idx + 2] if idx + 2 < len(state) else '.')
        )

        if neighborPattern in alivePatterns:
            newState[idx] = '#'
        else:
            newState[idx] = '.'

    # Increase state size if necessary
    if '#' in newState[:5]:
        newState = FIVE_DEAD + newState
        CURRENT_ZERO += 5
        print "CURRENT_ZERO", CURRENT_ZERO
    if '#' in newState[-5:]:
        newState += FIVE_DEAD

    return newState

with open('12_out.txt', 'w') as f:
    # Generations
    currentState = initialState
    for gen in range(1000):
        newState = newGen(currentState)

        # print(gen + 1), "\t", "".join(newState)
        idxSum = sum([
            idx - CURRENT_ZERO
            for (idx, cell) in enumerate(newState)
            if cell == '#'
        ])
        # print idxSum
        f.write(
            str(gen + 1) + ' ' + str(idxSum) + "\n"
        )
        currentState = newState

# We are at gen 1000
# By plotting into Octave we see that the growth has stabilized
# at a rate of +109 plants each gen

print sum([
    idx - CURRENT_ZERO
    for (idx, cell) in enumerate(currentState)
    if cell == '#'
]) + (50000000000 - 1000) * 109

# Answers submitted
# 1750000097165 (too low)
# 5450000001166 (✅)
# 6699999976166 (too high)
# 6699999998165 (too high)
