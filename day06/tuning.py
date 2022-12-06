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
# Find the first marker and pos
#
def findFirstMarker(buffer):

    return findMarker(buffer,4)


#
# Find the first message and pos
#
def findFirstMessage(buffer):

    return findMarker(buffer,14)


#
# Find the marker and pos
#
def findMarker(buffer, markerLen):

    markerPos = 0
    markerStr = ""

    for pos in range(0,len(buffer)-markerLen):
        marker = buffer[pos:pos+markerLen]
        #print(marker)
        isMarker = True
        for p in range(0,markerLen-1):
            c = marker[p]
            #print(c)
            if c in marker[p+1:markerLen]:
                isMarker = False
                break
        if isMarker:
            markerPos = pos + markerLen
            markerStr = marker
            break

    return markerPos, markerStr


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
    line = lines[0]
    firstMarkerPos, firstMarker = findFirstMarker(line)
    answer = firstMarkerPos
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    firstMarkerPos, firstMarker = findFirstMessage(line)
    answer = firstMarkerPos
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
