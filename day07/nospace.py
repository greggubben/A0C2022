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
    fileSystem = {"/": {}}
    cwd = fileSystem["/"]
    parentwd = [cwd]

    f = open(filename)
    for line in f:
        line = line.strip()
        lines.append(line)
        parts = line.split(" ");
        if parts[0] == "$":
            # Command
            #print("Command")
            if parts[1] == "cd":
                # Change directory
                #print("  change directory")
                if parts[2] == "/":
                    # to root
                    #print("    to root /")
                    cwd = fileSystem["/"]
                    parentwd = [fileSystem]
                elif parts[2] == "..":
                    # up 1 directory
                    #print("    up")
                    cwd = parentwd.pop()
                else:
                    # must be to a new sub-directory
                    #print("    down to", parts[2])
                    #print(fileSystem)
                    parentwd.append(cwd)
                    cwd = cwd[parts[2]]
            elif parts[1] == "ls":
                # Don't care about 'ls' commands
                #print("  ignore ls")
                pass
            else:
                print("  Unknown command:", parts[1])
        elif parts[0] == "dir":
            # results of ls command
            # this is a directory
            #print("Directory:", parts[1])
            cwd[parts[1]] = {}
        else:
            # this is a file
            #print("File:", parts[1], "size:", parts[0])
            cwd[parts[1]] = int(parts[0])

    f.close()

    return fileSystem, lines


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


#
# Print directory structure
#
def printDirectory(fileSystem, indent=0):

    for name, file in fileSystem.items():
        if type(file) is dict:
            fileType = "dir"
        else:
            fileType = "file, size=" + str(file)
        print(f"{' ' * indent}- {name} ({fileType})")

        if type(file) is dict:
            printDirectory(file,indent+2)


#
# Sum files
#
def sumFiles(fileSystem, directorySizes=[]):

    dirSize = 0

    for name, file in fileSystem.items():
        if type(file) is dict:
            directorySizes, size = sumFiles(file, directorySizes)
            dirSize += size
            directorySizes.append(size)
        else:
            dirSize += file

    return directorySizes, dirSize


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
    fileSystem, lines = loadData(filename)
    print(" Lines Read: ", len(lines))
    print()
    printLines(lines)

    # Do Part 1 work
    print()
    printDirectory(fileSystem)
    directorySizes, totalSize = sumFiles(fileSystem)
    print(directorySizes)
    answer = sum(s for s in directorySizes if s <= 100000)
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    freeSpace = 70000000 - totalSize
    print("Total Size:", totalSize)
    print(" Free Size:", freeSpace)
    directorySizes.sort()
    enough = [s for s in directorySizes if s + freeSpace >= 30000000]
    answer = enough[0]
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
