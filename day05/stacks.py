#
# Adavent of Code Template
#
import sys
import copy

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
    stacks = []
    moves = []

    loadingStacks = True
    initDone = False

    f = open(filename)
    for line in f:
        line = line.replace("\r","").replace("\n","")
        lines.append(line)

        if line == "":
            loadingStacks = False
        elif loadingStacks:
            # Loading the Stacks section of the input
            #print(len(line))
            if not initDone:
                # Initialise the Stacks
                numStacks = int((len(line) + 1)/4)
                #print("Stacks",numStacks)
                for s in range(0,numStacks):
                    stack = []
                    stacks.append(stack)
                initDone = True

            # load the stacks
            for s in range(0,len(stacks)):
                crate = line[s*4+1]
                #print("stack", s, "  crate", crate )
                if crate != " ":
                    stacks[s].insert(0,crate)
        else:
            # Loading the Moves section of the input
            mStr, qty, fStr, fromStack, tStr, toStack = line.split(" ")
            #print(qty, fromStack, toStack)
            moves.append((int(qty), int(fromStack), int(toStack)))

    f.close()

    return stacks, moves, lines


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


#
# Print Stacks
#
def printStacks(stacks, qty=0, newStack=0):

    maxCrates = max(len(stack) for stack in stacks)
    #print("maxCrates", maxCrates)

    for crateNum in range(maxCrates,1,-1):
        rowStr = ""
        for s, stack in enumerate(stacks):
            if len(stack) >= crateNum:
                if newStack-1 == s and qty > 0:
                    qty -= 1
                    rowStr += color.YELLOW
                rowStr += f"[{stack[crateNum-1]}] "
                rowStr += color.END
            else:
                rowStr += "    "
        print(rowStr)

    rowStr = ""
    for stack in stacks:
        rowStr += f" {stack[0]}  "
    print(rowStr)


#
# Print Moves
#
def printMoves(moves):

    for move in moves:
        print(f"move {move[0]} from {move[1]} to {move[2]}")


#
# Move Crates between Stacks
#
def moveCrates(moves, stacks):

    for move in moves:
        qty, fromStackNum, toStackNum = move
        fromStack = stacks[fromStackNum-1]
        toStack = stacks[toStackNum-1]
        for c in range(0,qty):
            crate = fromStack.pop()
            toStack.append(crate)

        print()
        #printStacks(stacks, qty, toStackNum)


#
# Move Multiple Crates between Stacks
#
def moveMultipleCrates(moves, stacks):

    for move in moves:
        qty, fromStackNum, toStackNum = move
        fromStack = stacks[fromStackNum-1]
        toStack = stacks[toStackNum-1]
        toLen = len(toStack)
        for c in range(0,qty):
            crate = fromStack.pop()
            toStack.insert(toLen,crate)

        print()
        printStacks(stacks, qty, toStackNum)


#
# Get top crate
#
def getTopCrates(stacks):

    topCrates = ""

    for stack in stacks:
        topCrates += stack[-1]

    return topCrates


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
    stacks, moves, lines = loadData(filename)
    print(" Lines Read: ", len(lines))
    print("Stacks Read: ", len(stacks))
    print(" Moves Read: ", len(moves))
    #print()
    #printLines(lines)
    print()
    #printStacks(stacks)
    print()
    #printMoves(moves)
    stacks2 = copy.deepcopy(stacks)

    # Do Part 1 work
    print()
    moveCrates(moves, stacks)
    answer = getTopCrates(stacks)
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    printStacks(stacks2)
    moveMultipleCrates(moves, stacks2)
    answer = getTopCrates(stacks2)
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
