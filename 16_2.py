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

possible_op = [set(OPERATIONS) for _ in range(16)]

with open("inputs/day16_1.txt") as f:
    myInput = f.read().strip().split('\n')

instructionsExamples = [_ for _ in myInput if len(_) > 0]

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

    for operation in OPERATIONS:
        if operation in possible_op[instr[0]]:
            _r = operation(beforeRegisters, instr[1], instr[2], instr[3])
            if tuple(afterRegisters) != _r:
                possible_op[instr[0]].remove(operation)

confirmed_opcode = set()

# If a opcode is confirmed (length of possible op == 1), remove that operation from the others
# Do that until you're sure of every opcode (which hopefully happens
# eventually)
while any([o not in confirmed_opcode and len(possible_op[o]) == 1 for o in range(16)]):
    o = [o for o in range(16) if o not in confirmed_opcode and len(
        possible_op[o]) == 1][0]
    oper = possible_op[o].pop()

    for _o in range(16):
        possible_op[_o].discard(oper)
    possible_op[o].add(oper)
    confirmed_opcode.add(o)

assert len(confirmed_opcode) == 16

# Now that we've confirmed every opcode, we can refactor or dict
possible_op = [_set.pop() for _set in possible_op]
assert len(possible_op) == len(set(possible_op))  # check for no duplicate

print possible_op

myInputProgram = myInput[3238:]

registers = (0, 0, 0, 0)
for line in myInputProgram:
    [opcode, inA, inB, outC] = [int(_) for _ in line.split(' ')]
    registers = possible_op[opcode](registers, inA, inB, outC)

print registers
