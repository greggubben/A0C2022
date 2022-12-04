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
# Assigned Sections
#
class Assignments:

    def __init__(self, s, e):
        self.start = s
        self.end = e

    def __str__(self):
        return f"{self.start}-{self.end}"


#
# Paired elf assignments
#
class Pairs:

    def __init__(self, f, s):
        self.first = f
        self.second = s
        if self.first.start  <= self.second.start and self.first.end  >= self.second.end or \
           self.second.start <= self.first.start  and self.second.end >= self.first.end:
               self.fullOverlap = True
        else:
               self.fullOverlap = False

        if self.first.start  <= self.second.start and self.second.start <= self.first.end or \
           self.first.start  <= self.second.end   and self.second.end   <= self.first.end or \
           self.second.start <= self.first.start  and self.first.start  <= self.second.end or \
           self.second.start <= self.first.end    and self.first.end    <= self.second.end:
               self.partOverlap = True
        else:
               self.partOverlap = False


    def __str__(self):
        return f"{self.first},{self.second}"


#
# Load the file into a data array
#
def loadData(filename):

    lines = []
    pairs = []

    f = open(filename)
    for line in f:
        line = line.strip()
        lines.append(line)
        assignments = [Assignments(int(pair.split("-")[0]), int(pair.split("-")[1])) for pair in line.split(",")]
        #print(assignments)
        pairs.append(Pairs(assignments[0], assignments[1]))

    f.close()

    return pairs, lines


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


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
    pairs, lines = loadData(filename)
    print(" Lines Read: ", len(lines))
    print()
    #printLines(lines)
    #printLines(pairs)

    # Do Part 1 work
    print()
    answer = sum( 1 for pair in pairs if pair.fullOverlap)
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    answer = sum( 1 for pair in pairs if pair.partOverlap)
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
