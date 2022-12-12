#
# Adavent of Code Template
#
import sys, math

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
    moves = []

    f = open(filename)
    for line in f:
        line = line.strip()
        lines.append(line)
        parts = line.split(" ")
        moves.append((parts[0],int(parts[1])))

    f.close()

    return moves, lines


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


#
# Print the Grid with positons
#
def printGrid (start, knotsPosition):

    maxKnotsX = max(x for (x,y) in knotsPosition)
    maxKnotsY = max(y for (x,y) in knotsPosition)
    minKnotsX = min(x for (x,y) in knotsPosition)
    minKnotsY = min(y for (x,y) in knotsPosition)

    maxX = int(max(start[0], maxKnotsX))
    maxY = int(max(start[1], maxKnotsY))
    minX = int(min(start[0], minKnotsX))
    minY = int(min(start[1], minKnotsY))

    #print("Max Tails: ", maxTailsX, maxTailsY,"Min Tails: ", minTailsX, minTailsY)
    #print("Max Heads: ", maxHeadsX, maxHeadsY,"Min Heads: ", minHeadsX, minHeadsY)
    #print("      Max: ", maxX, maxY,          "      Min: ", minX, minY)

    for y in range(maxY+1, minY-1, -1):
        rowStr = ""
        for x in range(minX, maxX+2):
            if (x,y) in knotsPosition:
                pos = knotsPosition.index((x,y))
                if pos == 0:
                    rowStr += color.YELLOW + "H" + color.END
                elif pos == len(knotsPosition)-1:
                    rowStr += color.YELLOW + "T" + color.END
                else:
                    rowStr += color.YELLOW + str(pos) + color.END
            elif x == start[0] and y == start[1]:
                rowStr += color.YELLOW + "s" + color.END
            else:
                rowStr += "."
        print(rowStr)


# (x,y)
directions = {"U": (0,1), "D": (0,-1), "L": (-1,0), "R": (1,0)}
#
# Move the rope
#
def moveRope (moves, numKnots):


    start = (0,0)

    knotsPosition = []
    knotsHistory = []
    for k in range(0,numKnots):
        knotsPosition.append(start)
        knotsHistory.append({start})

    #print("-- Initial State --")
    #printGrid(start, knotsPosition)

    for (direction, distance) in moves:
        #print()
        #print("==", direction, distance, "==")
        for d in range(1,distance+1):
            # Move the head
            (xChange, yChange) = directions[direction]
            (headX, headY) = knotsPosition[0]
            headX += xChange
            headY += yChange
            knotsPosition[0] = (headX, headY)
            knotsHistory[0].add((headX, headY))

            # Move the tails
            for k in range(1,numKnots):
                xChange = 0
                yChange = 0
                (tailX, tailY) = knotsPosition[k]
                if abs(headX - tailX) > 1:
                    xChange = math.copysign(1,(headX - tailX))
                    if abs(headY - tailY) > 0:
                        yChange = math.copysign(1,(headY - tailY))
                if abs(headY - tailY) > 1:
                    yChange = math.copysign(1,(headY - tailY))
                    if abs(headX - tailX) > 0:
                        xChange = math.copysign(1,(headX - tailX))
                tailX += xChange
                tailY += yChange
                knotsPosition[k] = (tailX, tailY)
                knotsHistory[k].add((tailX, tailY))
                headX = tailX
                headY = tailY

            #print()
            #printGrid(start, knotsPosition)

    return knotsHistory[0], knotsHistory[-1]

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
    moves, lines = loadData(filename)
    print(" Lines Read: ", len(lines))
    print()
    printLines(lines)

    # Do Part 1 work
    print()
    heads, tails = moveRope(moves,2)
    answer = len(tails)
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    heads, tails = moveRope(moves,10)
    answer = len(tails)
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
