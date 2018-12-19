from cpu_instructions import OPERATIONS_DICT

with open('inputs/day19_1.txt') as f:
    myInput = [_ for _ in f.read().split('\n') if len(_) > 0]

ip_reg = int(myInput[0][4:])
registers = [0, 0, 0, 0, 0, 0]
instructions = myInput[1:]

print "IP REG", ip_reg
print "#instructions", len(instructions)

tick = 0
while registers[ip_reg] <= len(instructions):
    next_instr = instructions[registers[ip_reg]]
    _verbose = registers[ip_reg] == 9 and registers[
        4] % 100 == 0 and registers[5] % 100 == 0

    if _verbose:
        print 't', tick, '#' + str(registers[ip_reg]), next_instr

    (op, inA, inB, outC) = next_instr.split(' ')
    newRegisters = OPERATIONS_DICT[op](
        registers, int(inA), int(inB), int(outC))
    registers = list(newRegisters)
    if _verbose:
        print registers
    registers[ip_reg] += 1

    tick += 1
    if _verbose:
        print "-----"

print registers
