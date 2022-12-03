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
# Find Dup
#
def findDups(lines):

    dupItems = []

    for line in lines:
        midpoint = int(len(line)/2)
        firstPart = line[0:midpoint]
        secondPart = line[midpoint:]
        item = "".join(c for c in firstPart if secondPart.find(c) != -1)[0]
        dupItems.append(item)
        #print (f"{firstPart} {secondPart} {item} {ord(item)-ord('a')+1}")

    return dupItems


#
# Find Groups
#
def findGroups(lines):

    groupItems = []

    for group in range(0,len(lines),3):
        firstSack = lines[group]
        secondSack = lines[group+1]
        thirdSack = lines[group+2]
        item = "".join(c for c in firstSack if secondSack.find(c) != -1 and thirdSack.find(c) != -1)[0]
        groupItems.append(item)
        print (f"{firstSack} {secondSack} {thirdSack} {item}")

    return groupItems


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
    dupItems = findDups(lines)
    answer = sum((ord(i)-ord('a')+1) if i >= 'a' else (ord(i)-ord('A')+27) for i in dupItems)
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    groupItems = findGroups(lines)
    answer = sum((ord(i)-ord('a')+1) if i >= 'a' else (ord(i)-ord('A')+27) for i in groupItems)
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
