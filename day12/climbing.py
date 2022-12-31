#
# Adavent of Code Template
#
import sys
import numpy as np
from scipy.sparse import dok_array
from scipy.sparse.csgraph import shortest_path
#import copy

# Global Variables

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


#
# Load the file into a data array
#
def loadData(filename):

    lines = []
    start = (0, 0)
    end = (0, 0)

    f = open(filename)
    for line in f:
        line = line.strip()
        if "S" in line:
            start = (line.index("S"), len(lines))
        if "E" in line:
            end = (line.index("E"), len(lines))

        lines.append(line)

    f.close()

    return start, end, lines


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


#
# compute the linear position of a coordinates
#
def getPos(y,x,maxX):
    return y*maxX + x


#
# Build a Dijkstra Array of steps
#
def buildDokSteps(heightmap):

    maxY = len(heightmap)
    maxX = len(heightmap[0])
    dimensions = maxY * maxX
    stepsArray = dok_array((dimensions, dimensions), dtype=np.int32)

    for y in range(maxY):
        for x in range(maxX):
            currentPos = getPos(y,x,maxX)
            currentAscii = ord(heightmap[y][x]) if heightmap[y][x] != "S" else ord("a")

            for (directionX, directionY) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:

                newX = x + directionX
                newY = y + directionY
                newPos = getPos(newY,newX,maxX)

                if 0 > newX or newX >= len(heightmap[0]) or \
                   0 > newY or newY >= len(heightmap):
                       # Out of range - skip it
                       continue

                newAscii = ord(heightmap[newY][newX])
                if heightmap[newY][newX] == "A":
                    newAscii = ord("a")
                elif heightmap[newY][newX] == "E":
                    newAscii = ord("z")

                #print("current",currentPos,heightmap[currentY][currentX],currentAscii, "new",newPos,heightmap[newY][newX],newAscii)

                if newAscii > currentAscii + 1:
                    # can't move to that position
                    #print("  no move")
                    continue

                # Must be OK to move
                stepsArray[currentPos, newPos] = 1

    return stepsArray


#
# Find all a starting points
#
def findAllStarts(heightmap):
    maxY = len(heightmap)
    maxX = len(heightmap[0])

    starts = []

    for y in range(maxY):
        for x in range(maxX):
            if heightmap[y][x] == "a":
                starts.append(getPos(y,x,maxX))

    return starts
        

#
# Find the fewest steps for each starting point
#
def findFewestSteps(possibleSteps, starts, endPos):

    fewestSteps = []

    for startPos in starts:
        dist_matrix = shortest_path(csgraph=possibleSteps, directed=True, indices=startPos, unweighted=True, return_predecessors=False)
        #print(dist_matrix)
        #print(fewestSteps)
        steps = dist_matrix[endPos]
        fewestSteps.append(steps)

    return fewestSteps


#
# Main
#
def main():

    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: " + sys.argv[0] + " inputfile");
        return
    filename = args[0]
    print("Input File:", filename)
    print()

    # Load data
    start, end, heightmap = loadData(filename)
    print(f"Heightmap size (x,y): ({len(heightmap[0])}, {len(heightmap)})")
    print("Start (x,y):", start)
    print("End (x,y):", end)
    print()
    #printLines(heightmap)

    possibleSteps = buildDokSteps(heightmap)
    startX, startY = start
    startPos = getPos(startY, startX, len(heightmap[0]))
    #print("Start Position (y,x) (", startY, ", ", startX, ")", startPos)
    endX, endY = end
    endPos = getPos(endY, endX, len(heightmap[0]))
    #print("End Position (y,x) (", endY, ", ", endX, ")", endPos)

    # Do Part 1 work
    print()
    starts = [startPos]
    fewestSteps = findFewestSteps(possibleSteps, starts, endPos) 
    answer = min(fewestSteps)
    #dist_matrix = shortest_path(csgraph=possibleSteps, directed=True, indices=startPos, unweighted=True, return_predecessors=False)
    #print(dist_matrix)
    #print(fewestSteps)
    #answer = dist_matrix[endPos]
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    starts = findAllStarts(heightmap)
    starts.append(startPos)
    #print(starts)
    fewestSteps = findFewestSteps(possibleSteps, starts, endPos) 
    answer = min(fewestSteps)
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
