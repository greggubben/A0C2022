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
# Print only if debugging
#
DEBUG = True
def debugPrint(s=""):
    if DEBUG:
        print(s)


#
# Load the file into a data array
#
def loadData(filename, sandSource):

    lines = []
    paths = []
    maxX = sandSource[0]
    minX = sandSource[0]
    maxY = sandSource[1]
    minY = sandSource[1]

    f = open(filename)
    for line in f:
        line = line.strip()
        lines.append(line)
        pointsStr = line.split(" -> ")
        path = []
        for pointStr in pointsStr:
            point = pointStr.split(",")
            x = int(point[0])
            y = int(point[1])
            path.append((x,y))
            maxX = max(maxX, x)
            minX = min(minX, x)
            maxY = max(maxY, y)
            minY = min(minY, y)
        paths.append(path)

    f.close()

    return paths, minX, maxX, minY, maxY


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(" -> ".join([str(x) + "," + str(y) for x,y in line]))


#
# Create the scan space
#
def initScan(minX, maxX, minY, maxY):

    offsetX = minX-1
    scan = ["."*(maxX-offsetX+2) for y in range(minY, maxY+1)]
    return scan, offsetX


#
# print the scan
#
def printScan(scan, offsetX):

    blankHeader = [" ", " ", " "]
    header = []
    startStr = list(str(offsetX))
    header.append(startStr)
    if scan[0].find("+") != -1:
        sourceX = offsetX + scan[0].find("+")
        header.extend([blankHeader] * (sourceX - offsetX - 1))
        sourceStr = list(str(sourceX))
        header.append(sourceStr)
        sourceX += 1
    else:
        sourceX = offsetX + 1
    endX = offsetX + len(scan[0])
    header.extend([blankHeader] * (endX - sourceX - 1))
    endStr = list(str(endX))
    header.append(endStr)

    for row in zip(*header):
        print("".join(row))

    for scanline in scan:
        printStr = scanline
        printStr = printStr.replace("+",color.CYAN + "+" + color.END)
        printStr = printStr.replace("#",color.RED + "#" + color.END)
        printStr = printStr.replace("o",color.YELLOW + "o" + color.END)
        print(printStr)


#
# set a value on Scan
#
def setPoint(scan, offsetX, point, value):

    x = point[0] - offsetX
    y = point[1]
    scan[y] = scan[y][:x] + value + scan[y][x+1:]


#
# get a value from Scan
#
def getPoint(scan, offsetX, point):

    x = point[0] - offsetX
    y = point[1]
    return scan[y][x]


#
# Draw Sand Source
#
def drawSandSource(scan, offsetX, sandSource):
    setPoint(scan, offsetX, sandSource, "+")


#
# Draw the paths
#
def drawPaths(scan, offsetX, paths):

    for path in paths:
        firstPoint = True
        #print("path", path)
        for point in path:
            #print("  point", point)
            if firstPoint:
                lastPoint = point
                firstPoint = False
                continue
            startX = min(lastPoint[0],point[0])
            endX = max(lastPoint[0],point[0])
            startY = min(lastPoint[1],point[1])
            endY = max(lastPoint[1],point[1])
            distance = max(endX-startX, endY-startY)
            deltaX = int((endX - startX)/max(endX-startX,1))
            deltaY = int((endY - startY)/max(endY-startY,1))
            #print("    startX", startX, "endX", endX, "startY", startY, "endY", endY)
            #print("    distance", distance, "deltaX", deltaX, "deltaY", deltaY)
            for d in range(distance+1):
                x = int(startX + deltaX*d)
                y = int(startY + deltaY*d)
                setPoint(scan, offsetX, (x,y), "#")
            lastPoint = point


#
# Have a grain of sand fall
#
def fallSand(scan, offsetX, sandStart):

    sandX = sandStart[0]
    sandY = sandStart[1]

    point = getPoint(scan, offsetX, (sandX, sandY))
    if point == "o":
        # blocked source - we are done
        return False

    while True:

        sandY += 1
        if sandY >= len(scan):
            # fell off the bottom - this sand will not stop
            return False

        point = getPoint(scan, offsetX, (sandX, sandY))

        if point == ".":
            # Keep falling
            continue
        else:
            # hit something - check if can fall to sides
            # fall to left first
            point = getPoint(scan, offsetX, (sandX-1, sandY))
            if point == ".":
                # ok to fall to left
                sandX = sandX - 1
                continue

            # fall to right
            point = getPoint(scan, offsetX, (sandX+1, sandY))
            if point == ".":
                # ok to fall to right
                sandX = sandX + 1
                continue

        # can't move anymore
        break

    sandY -= 1
    setPoint(scan, offsetX, (sandX, sandY), "o")

    # room for more sand
    return True


#
# Pour the sand until sand falls forever
#
def pourSand(scan, offsetX, sandSource):

    units = 0

    while fallSand(scan, offsetX, sandSource):
        units += 1

    return units


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
    sandSource = (500,0)
    paths, minX, maxX, minY, maxY = loadData(filename,sandSource)
    print(" Lines Read: ", len(paths))
    print("Min X:", minX, "Max X:",maxX)
    print("Min Y:", minY, "Max Y:",maxY)
    print()
    printLines(paths)

    # Do Part 1 work
    print()
    scan, offsetX = initScan(minX, maxX, minY, maxY)
    drawSandSource(scan, offsetX, sandSource)
    drawPaths(scan, offsetX, paths)
    sandUnits = pourSand(scan, offsetX, sandSource)
    printScan(scan, offsetX)
    answer = sandUnits
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    bottomY = maxY + 2
    bottomMinX = sandSource[0] - bottomY
    bottomMaxX = sandSource[0] + bottomY
    scan, offsetX = initScan(bottomMinX, bottomMaxX, minY, bottomY)
    drawSandSource(scan, offsetX, sandSource)
    paths.append([(bottomMinX, bottomY),(bottomMaxX, bottomY)])
    drawPaths(scan, offsetX, paths)
    sandUnits = pourSand(scan, offsetX, sandSource)
    printScan(scan, offsetX)
    answer = sandUnits
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
