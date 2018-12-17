elvesIdx = [0, 1]

recipes = [3, 7]

LIMIT = 9


def printRecipes(recipes):
    recStr = []
    for idx, rec in enumerate(recipes):
        if idx == elvesIdx[0]:
            recStr.append('(' + str(recipes[idx]) + ')')
        elif idx == elvesIdx[1]:
            recStr.append('[' + str(recipes[idx]) + ']')
        else:
            recStr.append(str(recipes[idx]))
    return ' '.join(recStr)

tick = 0
if LIMIT < 100:
    print 'tick', tick
    print printRecipes(recipes)

while len(recipes) <= LIMIT + 10:
    mySum = sum([recipes[idx] for idx in elvesIdx])
    if mySum >= 10:
        recipes.append(int(mySum / 10))
    recipes.append(mySum % 10)

    elvesIdx = [((idx + 1 + recipes[idx]) % len(recipes)) for idx in elvesIdx]
    tick += 1
    if LIMIT < 100:
        print 'tick', tick
        print printRecipes(recipes)

print ''.join([str(c) for c in recipes[LIMIT:LIMIT + 10]])
