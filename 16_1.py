import re


def addr(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = prevRegisters[inA] + prevRegisters[inB]
    return tuple(newRegisters)


def addi(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = prevRegisters[inA] + inB
    return tuple(newRegisters)


def mulr(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = prevRegisters[inA] * prevRegisters[inB]
    return tuple(newRegisters)


def muli(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = prevRegisters[inA] * inB
    return tuple(newRegisters)


def banr(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = prevRegisters[inA] & prevRegisters[inB]
    return tuple(newRegisters)


def bani(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = prevRegisters[inA] & inB
    return tuple(newRegisters)


def borr(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = prevRegisters[inA] | prevRegisters[inB]
    return tuple(newRegisters)


def bori(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = prevRegisters[inA] | inB
    return tuple(newRegisters)


def setr(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = prevRegisters[inA]
    return tuple(newRegisters)


def seti(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = inA
    return tuple(newRegisters)


def gtir(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = 1 if inA > prevRegisters[inB] else 0
    return tuple(newRegisters)


def gtri(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = 1 if prevRegisters[inA] > inB else 0
    return tuple(newRegisters)


def gtrr(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = 1 if prevRegisters[inA] > prevRegisters[inB] else 0
    return tuple(newRegisters)


def eqir(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = 1 if inA == prevRegisters[inB] else 0
    return tuple(newRegisters)


def eqri(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = 1 if prevRegisters[inA] == inB else 0
    return tuple(newRegisters)


def eqrr(prevRegisters, inA, inB, outC):
    newRegisters = list(prevRegisters)
    newRegisters[outC] = 1 if prevRegisters[inA] == prevRegisters[inB] else 0
    return tuple(newRegisters)


OPERATIONS = [
    addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri,
    gtrr, eqir, eqri, eqrr,
]

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
