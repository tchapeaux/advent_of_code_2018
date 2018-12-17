import re
from collections import namedtuple

with open('inputs/day4_1.txt') as f:
    parsedInput = f.readlines()

parsedInput = [x.strip() for x in parsedInput if len(x.strip()) > 0]

recordRegex = r"^\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{02})\] (.*)"
beginShiftRegex = r".*#(\d*).*"

dates = []

# First pass : parse data by day

for record in sorted(parsedInput):
    m = re.match(recordRegex, record)
    assert m
    (yyyy, MM, dd, hh, mm, recordMessage) = m.groups()
    # print(yyyy, MM, dd, hh, mm, recordMessage)
    assert yyyy == '1518'

    if 'begins shift' in recordMessage:
        m2 = re.match(beginShiftRegex, recordMessage)
        assert m2
        (guardID, ) = m2.groups()

        isNextDay = int(hh) > 1
        calendarDay = (
            MM + "-" + str(int(dd) + (1 if isNextDay else 0)).zfill(2))

        dates.append({
            'calendarDay': calendarDay,
            'guardID': guardID,
            'minutesAsleep': []
        })

    elif 'falls asleep' in recordMessage:
        assert len(dates) > 0
        date = dates[-1]
        date['minutesAsleep'].append(int(mm))

    elif 'wakes up' in recordMessage:
        assert len(dates) > 0
        date = dates[-1]
        minuteAsleep = date['minutesAsleep'][-1]
        for minute in range(int(minuteAsleep) + 1, int(mm)):
            date['minutesAsleep'].append(minute)

# print dates

# Second pass: re-arrange data by guard

guards = {}  # dict of guardID

for date in dates:
    guardID = date['guardID']
    if guardID not in guards:
        guards[guardID] = {'minutesSleepCnt': {}}
    guard = guards[guardID]

    for minute in range(60):
        if minute in date['minutesAsleep']:
            if (minute not in guard['minutesSleepCnt']):
                guard['minutesSleepCnt'][minute] = 0
            guard['minutesSleepCnt'][minute] += 1

# Analyse guards list to find most asleep (most minutes slept)

currentMostAsleepTime = 0
currentMostAsleepID = None
for (guardID, guard) in guards.items():
    minutesAsleep = sum(guard['minutesSleepCnt'].values())
    if minutesAsleep > currentMostAsleepTime:
        currentMostAsleepTime = minutesAsleep
        currentMostAsleepID = guardID

mostAsleepTime = currentMostAsleepTime
mostAsleepID = currentMostAsleepID

# Find most asleep minute for most asleep guard

assert mostAsleepID in guards
mostAsleepGuard = guards[mostAsleepID]
(_mostAsleepMinuteCnt, mostAsleepMinute) = max(
    [(val, idx) for (idx, val) in mostAsleepGuard['minutesSleepCnt'].items()])

print "most asleed ID", mostAsleepID
print "most asleep at minute", mostAsleepMinute
print "=>", int(mostAsleepID) * int(mostAsleepMinute)
