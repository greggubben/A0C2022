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
    elves = []
    calories = []

    f = open(filename)
    for line in f:
        line = line.strip()
        lines.append(line)
        if line == "":
            elves.append(calories)
            calories = []
        else:
            calories.append(int(line))

    if len(calories) != 0:
        elves.append(calories)

    f.close()

    return lines, elves


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


#
# Print Elves
#
def printElves(elves):

    for elf in elves:
      print(elf)


#
# Sum Calories
#
def sumCalories(elves):

    elvesCalories = []

    for elf in elves:
        elfCalories = 0
        for itemCalories in elf:
            elfCalories += itemCalories
        elvesCalories.append(elfCalories)

    return elvesCalories


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
    lines, elves = loadData(filename)
    print(" Lines Read: ", len(lines))
    print()
    #printLines(lines)
    #printElves(elves)

    # Do Part 1 work
    print()
    elvesCalories = sumCalories(elves)
    answer = max(elvesCalories)
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    elvesCalories.sort(reverse=True)
    answer = sum(elvesCalories[0:3])
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
