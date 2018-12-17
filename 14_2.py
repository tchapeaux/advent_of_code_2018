elvesIdx = [0, 1]

recipes = [3, 7]

BACKSTOP = '320851'


def printRecipes():
    recStr = []
    for idx, rec in enumerate(recipes):
        if idx == elvesIdx[0]:
            recStr.append('(' + str(recipes[idx]) + ')')
        elif idx == elvesIdx[1]:
            recStr.append('[' + str(recipes[idx]) + ']')
        else:
            recStr.append(str(recipes[idx]))
    return ' '.join(recStr)


def hasBackstop():
    for offset in range(3):
        _r = recipes[-len(BACKSTOP) - offset:-offset]
        _r = ''.join([str(c) for c in _r])
        if _r == BACKSTOP:
            return True
    return False

tick = 0
if False:
    print 'tick', tick
    print printRecipes()

while not hasBackstop():
    mySum = sum([recipes[idx] for idx in elvesIdx])
    if mySum >= 10:
        recipes.append(int(mySum / 10))
    recipes.append(mySum % 10)

    elvesIdx = [((idx + 1 + recipes[idx]) % len(recipes)) for idx in elvesIdx]
    tick += 1
    if False and tick % 1000 == 0:
        print 'tick', tick, len(recipes)
        # print printRecipes()

print ''.join([str(c) for c in recipes]).find(BACKSTOP)
