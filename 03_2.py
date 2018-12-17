import re

with open('inputs/day3_1.txt') as f:
  parsedInput = f.readlines()

parsedInput = [x.strip() for x in parsedInput if len(x.strip()) > 0]

claimRegex = r"#(\d*) @ (\d*),(\d*): (\d*)x(\d*)"

# Data structure for the fabric
# Shallow matrix / sparce grid (dict of dict)
# fabric[x][y] = nb of claims
fabric = {}

# Helper functions

def cellValue(fabric, x, y):
  return fabric[x][y] if x in fabric and y in fabric[x] else 0

def printFabric(fabric, maxWidth, maxHeight):
  fabricStr = ''

  # Here we need to loop first on the y because we will draw the
  # Grid row by row
  for y in range(maxHeight):
    for x in range(maxWidth):
      cell = cellValue(fabric, x, y)
      fabricStr += str(cell) if cell else '.'
    fabricStr += '\n'
  print fabricStr

def mark_overlaped(fabric, claimID):
  # Replace all occurrences of claimID with X
  for x in fabric.keys():
    for y in fabric[x].keys():
      if fabric[x][y] == claimID:
        fabric[x][y] = 'X'

# Mark cells with number of occurrences
for claim in parsedInput:
  #  print claim
  m = re.match(claimRegex, claim)
  assert m
  (claimID, left, top, width, height) = m.groups()

  # flag variable
  has_overlapped = False

  for _dx in range(int(width)):
    x = int(left) + _dx
    for _dy in range(int(height)):
      y = int(top) + _dy
      if x not in fabric:
        fabric[x] = {}
      if y not in fabric[x]:
        fabric[x][y] = claimID
      else:
        # Overlap detected
        # Flag this claim as overlapping
        has_overlapped = True

        # Mark previous claim as overlapping (replace their ID by X)
        overlapping_claim = fabric[x][y]
        if (overlapping_claim != 'X'):
          mark_overlaped(fabric, fabric[x][y])
      # print "cell at", x, ",", y, "is now", fabric[x][y]

  # If the claim was marked as overlapping while placing cells, mark it immediately as overlapping
  if has_overlapped:
    mark_overlaped(fabric, claimID)


maxWidth = max(fabric.keys()) + 1
maxHeight = max(max(row.keys()) for row in fabric.values()) + 1

print 'MAX', maxWidth, maxHeight

if (maxWidth < 100 and maxHeight < 100):
  printFabric(fabric, maxWidth, maxHeight)

# Find the first cell with a non-overlapped and non-null value
for x in fabric.keys():
  for y in fabric.keys():
    cell = cellValue(fabric, x, y)
    if cell and cell != 'X':
      print 'claim ID', cell
      # UGLY : we should break gracefully here
