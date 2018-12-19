import re

from cpu_instructions import OPERATIONS

with open("inputs/day16_1.txt") as f:
    myInput = f.read().strip().split('\n')

instructionsExamples = [_ for _ in myInput if len(_) > 0]

samplesMatches3Count = 0
for idx in range(0, len(instructionsExamples) / 3):
    if not instructionsExamples[3 * idx].startswith('Before:'):
        break

    in_before = instructionsExamples[3 * idx][8:]
    in_instr = instructionsExamples[3 * idx + 1]
    in_after = instructionsExamples[3 * idx + 2][8:]

    registerRegex = r"\[(\d)*, (\d*), (\d)*, (\d)*\]"
    before_match = re.match(registerRegex, in_before)
    after_match = re.match(registerRegex, in_after)
    assert before_match and after_match

    beforeRegisters = [int(_) for _ in before_match.groups()]
    afterRegisters = [int(_) for _ in after_match.groups()]
    instr = [int(_) for _ in in_instr.split(' ')]
    assert len(beforeRegisters) == 4
    assert len(afterRegisters) == 4
    assert len(instr) == 4

    print "before:", beforeRegisters
    print "instr:", instr
    print "after:", afterRegisters

    possibleCount = 0
    for operation in OPERATIONS:
        print "operation", operation
        _r = operation(beforeRegisters, instr[1], instr[2], instr[3])
        print "gives register", _r
        if tuple(afterRegisters) == _r:
            print "!!! match"
            possibleCount += 1

    if possibleCount >= 3:
        samplesMatches3Count += 1

print samplesMatches3Count

# Previous answers
# 155 (too low)
# 614 OK
