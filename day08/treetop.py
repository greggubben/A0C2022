#
# Adavent of Code Template
#
import sys

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

    f = open(filename)
    for line in f:
        line = line.strip()
        lines.append(line)

    f.close()

    return lines


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


#
# Get Trees going to bottom edge
#
def getBottomTrees(trees, row, col):

    return [trees[r][col] for r in range(row,len(trees))]


#
# Get Trees going to top edge
#
def getTopTrees(trees, row, col):

    return [trees[r][col] for r in range(row,-1,-1)]


#
# Get Trees going to left edge
#
def getLeftTrees(trees, row, col):

    return [trees[row][c] for c in range(col,-1,-1)]


#
# Get Trees going to right edge
#
def getRightTrees(trees, row, col):

    return [trees[row][c] for c in range(col,len(trees[row]))]


#
# Check if trees are visible (lower)
#
def checkVisible(toEdge, debugLabel = "  "):

    visible = True

    if toEdge[0] <= max(toEdge[1:]):
        visible = False

    #print(debugLabel,toEdge, visible)

    return visible


#
# Compuet the scenic score for a line of trees
#
def viewingDistance(toEdge, debugLabel = ""):

    score = 0

    for t in toEdge[1:]:

        if toEdge[0] > t:
            score += 1
        else:
            score += 1
            break

    #print(debugLabel,toEdge, score)

    return score


#
# Find the interior trees that are visible
#
def findVisibleInterior(trees):

    visibleTrees = 0

    for y in range(1,len(trees)-1):

        for x in range(1,len(trees[y])-1):

            #print("Check (", y, " x ", x, ") = ", trees[y][x])
            #checkVisible(getTopTrees   (trees, y, x), "     Top")
            #checkVisible(getBottomTrees(trees, y, x), "  Bottom")
            #checkVisible(getLeftTrees  (trees, y, x), "    Left")
            #checkVisible(getRightTrees (trees, y, x), "   Right")

            if checkVisible(getTopTrees   (trees, y, x), "     Top") or \
               checkVisible(getBottomTrees(trees, y, x), "  Bottom") or \
               checkVisible(getLeftTrees  (trees, y, x), "    Left") or \
               checkVisible(getRightTrees (trees, y, x), "   Right"):

                #print("Visible:",y," x ",x)
                visibleTrees += 1

    return visibleTrees


#
# Find the scenic score for each of the interior trees
#
def findScenicScores(trees):

    scenicScores = []

    for y in range(1,len(trees)-1):

        for x in range(1,len(trees[y])-1):
            #print("Score (", y, " x ", x, ") = ", trees[y][x])
            score = viewingDistance(getTopTrees   (trees, y, x), "     Top") * \
                    viewingDistance(getBottomTrees(trees, y, x), "  Bottom") * \
                    viewingDistance(getLeftTrees  (trees, y, x), "    Left") * \
                    viewingDistance(getRightTrees (trees, y, x), "   Right")

            scenicScores.append(score)


    return scenicScores


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
    lines = loadData(filename)
    print(" Lines Read: ", len(lines))
    print()
    printLines(lines)

    print(f"{len(lines[0])} x {len(lines)} grid")

    # Do Part 1 work
    print()
    interiorVisible = findVisibleInterior(lines)
    answer = (len(lines[0])*2) + ((len(lines)-2)*2) + interiorVisible
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    scenicScores = findScenicScores(lines)
    answer = max(scenicScores)
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
