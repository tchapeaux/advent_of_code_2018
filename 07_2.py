# CONSTANTS

INPUT_PATH = 'inputs/day7_1.txt'
NB_OF_WORKERS = 5
BASE_TIME = 60

# Helper functions


def taskTime(task):
    return BASE_TIME + (ord(task) - ord('A')) + 1


def nbOfDependencies(task):
    return len(tasks[task])


def finishTask(task):
    orderOfCompletion.append(task)
    # Remove task from dependencies
    for t in tasks.keys():
        tasks[t] = [d for d in tasks[t] if d is not task]


def getNextReadyTask(tasks):
    readyTasks = [
        t for t in tasks.keys()
        if nbOfDependencies(t) == 0
        and t not in orderOfCompletion
        and t not in [w["task"] for w in workers]
    ]
    nextTask = min(readyTasks) if len(readyTasks) > 0 else None
    return nextTask


def isBusy(worker):
    return worker['timeLeft'] > 0


def makeWork(worker):
    if isBusy(worker):
        worker['timeLeft'] -= 1

# Parse input
with open(INPUT_PATH) as f:
    parsedInput = f.read().strip().split('\n')

inputDependencies = [(i[5], i[36]) for i in parsedInput]
tasks = {}

for (source, dest) in inputDependencies:
    if source not in tasks:
        tasks[source] = []
    if dest not in tasks:
        tasks[dest] = []

    tasks[dest].append(source)

# Let's go

workers = [
    {
        "idx": idx,
        "timeLeft": 0,
        "task": None
    } for idx in range(NB_OF_WORKERS)
]
tick = 0

orderOfCompletion = []


while len(orderOfCompletion) < len(tasks.keys()):
    # New tick

    # Make workers work
    busyWorkers = [w for w in workers if isBusy(w)]
    for w in busyWorkers:
        makeWork(w)
        if w['timeLeft'] == 0:
            finishTask(w['task'])
            w['task'] = None

    # Assign tasks to free workers
    freeWorkers = [w for w in workers if not isBusy(w)]
    for freeW in freeWorkers:
        nextTask = getNextReadyTask(tasks)
        if (nextTask):
            freeW["task"] = nextTask
            freeW["timeLeft"] = taskTime(nextTask)

    print "tick", tick, "\t", "\t".join([worker["task"] if isBusy(worker) else '.' for worker in workers]), "".join(orderOfCompletion)
    tick += 1


# beware of OBO error (we count one tick too much)
print "final tick", tick - 1
