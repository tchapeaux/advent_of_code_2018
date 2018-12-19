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

OPERATIONS_DICT = {
    "addr": addr, "addi": addi, "mulr": mulr, "muli": muli, "banr": banr,
    "bani": bani, "borr": borr, "bori": bori, "setr": setr, "seti": seti,
    "gtir": gtir, "gtri": gtri, "gtrr": gtrr, "eqir": eqir, "eqri": eqri,
    "eqrr": eqrr
}
