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

# Mark cells with number of occurrences
for claim in parsedInput:
  #  print claim
  m = re.match(claimRegex, claim)
  assert m
  (claimId, left, top, width, height) = m.groups()

  for _dx in range(int(width)):
    x = int(left) + _dx
    for _dy in range(int(height)):
      y = int(top) + _dy
      if x not in fabric:
        fabric[x] = {}
      if y not in fabric[x]:
        fabric[x][y] = 0
      fabric[x][y] += 1
      # print "cell at", x, ",", y, "is now", fabric[x][y]

maxWidth = max(fabric.keys()) + 1
maxHeight = max(max(row.keys()) for row in fabric.values()) + 1

print 'MAX', maxWidth, maxHeight

if (maxWidth < 100 and maxHeight < 100):
  printFabric(fabric, maxWidth, maxHeight)

duplicateCnt = 0
for x in range(maxWidth):
  for y in range(maxHeight):
    cell = cellValue(fabric, x, y)
    duplicateCnt += 1 if cell and cell > 1 else 0

print 'duplicate', duplicateCnt

print "---- Wrong answers"
print "116268 (too small)"
