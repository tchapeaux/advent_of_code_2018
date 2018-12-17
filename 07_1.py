with open('inputs/day7_example.txt') as f:
    parsedInput = f.read().strip().split('\n')

inputDependencies = [(i[5], i[36]) for i in parsedInput]

print inputDependencies

# Do a linked list probably (because it looks like it)
# Let's also have a dict to each node

tasks = {}

for (source, dest) in inputDependencies:
    if source not in tasks:
        tasks[source] = []
    if dest not in tasks:
        tasks[dest] = []

    tasks[dest].append(source)


def nbOfDependencies(task):
    return len(tasks[task])


def isReady(task):
    return nbOfDependencies(task) == 0

orderOfCompletion = []

print "go"

while len(orderOfCompletion) < len(tasks.keys()):
    unfinishedTasks = [t for t in tasks if t not in orderOfCompletion]
    print "== ", unfinishedTasks
    readyTasks = [t for t in unfinishedTasks if isReady(t)]
    print "which are ready?", readyTasks
    nextTask = min(readyTasks)
    print "choose", nextTask
    orderOfCompletion.append(nextTask)

    # Remove task from dependencies
    for t in tasks.keys():
        tasks[t] = [d for d in tasks[t] if d is not nextTask]


print "".join(orderOfCompletion)
