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
# process instructions
#
def processInstructions(instructions):

    x = 1
    xValues = []

    for instruction in instructions:
        #print(instruction, "X=", x, "cycle=", len(xValues))
        parts = instruction.split(" ")
        if parts[0] == "noop":
            xValues.append(x)
        elif parts[0] == "addx":
            xValues.append(x)
            xValues.append(x)
            x += int(parts[1])

    xValues.append(x)
    return xValues


#
# turn on or off each pixel on the crt based on x values
#
def drawSprites(xValues):

    crt = []

    crtRow = ""
    for cycle in range(0,240):

        pos = cycle%40

        if pos == 0 and cycle != 0:
            crt.append(crtRow)
            crtRow = ""

        x = xValues[cycle]
        if x -1 <= pos and pos <= x+1:
            crtRow += "#"
        else:
            crtRow += "."

    crt.append(crtRow)

    return crt


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

    # Do Part 1 work
    print()
    xValues = processInstructions(lines)
    #for x in range(20,221,40):
    #    print("X=", x)
    #    print("xValue =", xValues[x-1])
    #    print("signal =", xValues[x-1]*x)
    answer = sum(xValues[x-1]*x for x in range(20,221,40))
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    crt = drawSprites(xValues)
    for row in crt:
        print(row)
    #answer = "X"
    #print()
    #print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
