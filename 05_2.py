with open('inputs/day5_1.txt') as f:
    parsedInput = f.read().strip()

input_data = [c for c in parsedInput]


def reacted_size(input_data):
    data = [c for c in input_data]
    is_clean = False  # H4CK to get into the loop
    while not is_clean:
        # Go through input from the end
        idx = len(data) - 2  # start at the second-to-last element
        is_clean = True

        while(idx >= 0):
            cur = data[idx]
            nxt = data[idx + 1]
            if (cur.islower() and nxt == cur.upper()) or (cur.isupper() and nxt == cur.lower()):
                # Pop two elements
                data.pop(idx + 1)
                data.pop(idx)

                is_clean = False
                idx -= 1
            idx -= 1

    return len(data)

size_by_letter = {}
for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    filtered_data = [
        c for c in input_data
        if c != letter and c != letter.lower()
    ]
    size_by_letter[letter] = reacted_size(filtered_data)
    print "letter", letter
    print "size", size_by_letter[letter]

print size_by_letter
print min(size_by_letter.values())
