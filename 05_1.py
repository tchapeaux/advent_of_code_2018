with open('inputs/day5_1.txt') as f:
    parsedInput = f.read().strip()

data = [c for c in parsedInput]

print "Input", data if len(data) < 100 else '', len(data)

is_clean = False  # H4CK to get into the loop
while not is_clean:
    # Go through input from the end
    idx = len(data) - 2  # start at the second-to-last element
    is_clean = True

    while(idx >= 0):
        cur = data[idx]
        nxt = data[idx + 1]
        if (cur.islower() and nxt == cur.upper()) or (cur.isupper() and nxt == cur.lower()):
            print "\tremoving", cur, nxt
            # Pop two elements
            data.pop(idx + 1)
            data.pop(idx)

            is_clean = False
            idx -= 1
        idx -= 1
    print "end of new pass - ", data if len(data) < 100 else '', len(data)

print "final pass", data if len(data) < 100 else '', len(data)
