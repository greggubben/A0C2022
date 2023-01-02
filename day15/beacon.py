#!/usr/bin/python3
#
# Adavent of Code Template
#
import sys
import time
from datetime import datetime


# Global Variables

class color:
   BLACK = '\033[30m'
   RED = '\033[31m'
   BRIGHTRED = '\033[91m'
   GREEN = '\033[32m'
   BRIGHTGREEN = '\033[92m'
   YELLOW = '\033[33m'
   BRIGHTYELLOW = '\033[93m'
   BLUE = '\033[34m'
   BRIGHTBLUE = '\033[94m'
   MAGENTA = '\033[35m'
   PURPLE = '\033[95m'
   CYAN = '\033[36m'
   BRIGHTCYAN = '\033[96m'
   WHITE = '\033[37m'
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
# Class for Sensor info and logic
#
class Sensor:

    def __init__(self, sensorX, sensorY, beaconX, beaconY):
        self.sensorX = int(sensorX)
        self.sensorY = int(sensorY)
        self.beaconX = int(beaconX)
        self.beaconY = int(beaconY)
        self.manhattenDistance = abs(self.sensorX - self.beaconX) + abs(self.sensorY - self.beaconY)
        self.minX = self.sensorX - self.manhattenDistance
        self.maxX = self.sensorX + self.manhattenDistance
        self.minY = self.sensorY - self.manhattenDistance
        self.maxY = self.sensorY + self.manhattenDistance


    def __str__(self):
        return f"Sensor at x={self.sensorX}, y={self.sensorY}: closest beacon is at x={self.beaconX}, y={self.beaconY}, distance={self.manhattenDistance}"


    def sensorOccupied(self, x, y):
        return (self.sensorX == x and self.sensorY == y)

    def beaconOccupied(self, x, y):
        return (self.beaconX == x and self.beaconY == y)

    def occupied(self, x, y):
        return (self.sensorOccupied(x,y) or self.beaconOccupied(x,y))

    def inRange(self, x, y):
        return (abs(self.sensorX - x) + abs(self.sensorY - y)) <= self.manhattenDistance

    def rowRange(self, y):
        xDist = self.manhattenDistance - abs(self.sensorY - y)
        return xDist >= 0, self.sensorX - xDist, self.sensorX + xDist


#
# Load the file into a data array
#
def loadData(filename):

    sensors = []

    f = open(filename)
    for line in f:
        line = line.strip()
        sensor, beacon = line.split(":")
        sensorX = sensor[sensor.find("x=")+2:sensor.find(",")]
        sensorY = sensor[sensor.find("y=")+2:]
        beaconX = beacon[beacon.find("x=")+2:beacon.find(",")]
        beaconY = beacon[beacon.find("y=")+2:]
        #print(sensorX, sensorY, beaconX, beaconY)
        sensors.append(Sensor(sensorX, sensorY, beaconX, beaconY))

    f.close()

    return sensors


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


#
# Print Grid old
#
def printGridOld(minX, maxX, minY, maxY, sensors):

    blankHeader = [" ", " ", " "]
    header = []
    for x in range(minX, maxX+1):
        if x%5 == 0:
            h = list(str(f"{x: 3}"))
            header.append(h)
        else:
            header.append(blankHeader)
    for row in zip(*header):
        print("    " + "".join(row))

    for y in range(minY, maxY+1):
        printStr = ""
        for x in range(minX, maxX+1):
            pointChar = "."

            for sensor in sensors:
                if sensor.sensorOccupied(x,y):
                    pointChar = "S"
                    break
                elif sensor.beaconOccupied(x,y):
                    pointChar = "B"
                    break
                elif sensor.inRange(x,y):
                    pointChar = "#"
                    break

            if pointChar in ["S", "B"]:
                pointChar = color.BRIGHTGREEN + pointChar + color.END
            elif x%5 == 0:
                pointChar = color.YELLOW + pointChar + color.END
            printStr += pointChar

        print(f"{y: 3} {printStr}")


#
# Print the grid
#
def printGrid(minX, maxX, minY, maxY, sensors):

    blankHeader = [" ", " ", " "]
    header = []
    for x in range(minX, maxX+1):
        if x%5 == 0:
            h = list(str(f"{x: 3}"))
            header.append(h)
        else:
            header.append(blankHeader)
    for row in zip(*header):
        print("    " + "".join(row))


    for y in range(minY,maxY+1):
        printStr = createRow(minX, maxX, y, sensors)

        xPos = len(printStr)
        for x in range(maxX, minX-1, -1):
            xPos -= 1
            if printStr[xPos] in ["S", "B"]:
                printStr = printStr[:xPos] + color.BRIGHTGREEN + printStr[xPos] + color.END + printStr[xPos+1:]
            elif x%5 == 0:
                printStr = printStr[:xPos] + color.YELLOW + printStr[xPos] + color.END + printStr[xPos+1:]

        print(f"{y: 3} {printStr}")


#
# find scanned positions
#
def findRowRanges(sensors, minX, maxX, row):

    rowStr = ""

    sensorRangeX = []
    sensorPositionX = []
    beaconPositionX = []

    for sensor in sensors:
        inRange, startX, endX = sensor.rowRange(row)
        if not inRange or endX < minX or startX > maxX:
            # not in range
            continue
        startX = max(startX, minX)
        endX = min(endX, maxX)
        sensorRangeX.append((startX, endX))
        if sensor.sensorY == row and minX <= sensor.sensorX and sensor.sensorX <= maxX:
            sensorPositionX.append(sensor.sensorX)
        if sensor.beaconY == row and minX <= sensor.beaconX and sensor.beaconX <= maxX:
            beaconPositionX.append(sensor.beaconX)

    #print(sensorRangeX)
    sensorRangeX.sort()
    #print(sensorRangeX)
    sensorPositionX.sort()
    beaconPositionX.sort()

    # remove overlaps in ranges
    consolidatedSensorRangeX = []
    if len(sensorRangeX) > 0:
        lastStartX,lastEndX = sensorRangeX[0]
        for startX,endX in sensorRangeX:
            if startX > lastEndX:
                # new range
                consolidatedSensorRangeX.append((lastStartX, lastEndX))
                lastStartX = startX
                lastEndX = endX
            elif endX > lastEndX:
                # extend range
                lastEndX = endX

        consolidatedSensorRangeX.append((lastStartX, lastEndX))

    return consolidatedSensorRangeX, sensorPositionX, beaconPositionX


#
# Create a row
#
def createRow(minX, maxX, y, sensors):

    printStr = ""
    sensorRangeX, sensorPositionX, beaconPositionX = findRowRanges(sensors, minX, maxX, y)
    #print("sensorRangeX=", sensorRangeX)
    #print("sensorPositionX=", sensorPositionX)
    #print("beaconPositionX=", beaconPositionX)
    x = minX
    for startX, endX in sensorRangeX:
        if x < startX:
            xLen = startX - x
            #print("x=", x, "startX=", startX, "xLen=", xLen)
            printStr += "." * xLen
            x += xLen
        xLen = endX - startX + 1
        printStr += "#" * xLen
        x += xLen

    xLen = maxX - x + 1
    printStr += "." * xLen

    for sensorX in sensorPositionX:
        xPos = sensorX - minX
        printStr = printStr[:xPos] + "S" + printStr[xPos+1:]

    for beaconX in beaconPositionX:
        xPos = beaconX - minX
        printStr = printStr[:xPos] + "B" + printStr[xPos+1:]

    return printStr


#
# Count the number of positions where a beacon cannot possibly exist
#
def countNoBeaconRow(sensors, minX, maxX, row):

    rowStr = createRow(minX, maxX, row, sensors)
    count = rowStr.count("#")
    #rowStr = f" {row: 3} "

    #print("minX:", minX, "maxX:", maxX)

    #sensorRangeX, sensorPositionX, beaconPositionX = findRowRanges(sensors, minX, maxX, row)
    #for x in range(minX, maxX+1):
    #    freeSpace = False
    #    inRangeSensors = []
    #    pointChar = "."
    #    for sensor in sensors:
    #        if sensor.inRange(x,row):
    #            inRangeSensors.append(sensor)
    #            freeSpace = True

    #    for sensor in inRangeSensors:
    #        if sensor.occupied(x,row):
    #            freeSpace = False
    #            pointChar = "X"
    #            break

    #    if freeSpace:
    #        count += 1
    #        pointChar = "#"
    #    rowStr += pointChar

    #print(rowStr)
    return count


#
# find scanned positions
#
def findScannedPositions(sensors, minX, maxX, row):

    rowStr = ""

    sensorRangeX, sensorPositionX, beaconPositionX = findRowRanges(sensors, minX, maxX, row)
    #print("minX:", minX, "maxX:", maxX)

    x = minX
    while x <= maxX:
        #print("x=", x)
        freeSpace = False
        pointChar = "."
        for sensor in sensors:
            if sensor.inRange(x,row):
                startX, endX = sensor.rowRange(row)
                #print("startX=", startX, "endX", endX)
                if startX != -1:
                    xLen = endX - max(x, startX) + 1
                    #print("xLen=", xLen)
                    pointChar = "#" * xLen
                    break
        x += len(pointChar)
        rowStr += pointChar
        #print(rowStr)

    rowStr += f" {row: }"
    #print(rowStr)
    return rowStr


#
# Find the distressed beacon with search range
#
def findDistressBeacon(sensors, minX, maxX, minY, maxY):

    #lastRowStr = findScannedPositions(sensors, minX, maxX, minY-1)
    lastRowStr = createRow(minX, maxX, minY-1, sensors)
    for y in range(minY, maxY+1):

        if y%1000 == 0:
            print(y)

        #rowStr = findScannedPositions(sensors, minX, maxX, y)
        rowStr = createRow(minX, maxX, y, sensors)
        distressX = rowStr.find("#.#")
        #print(distressX)
        if distressX != -1:
            # the plus 1 is for the starting #
            distressX += 1
            print("distress x=", distressX, "y=", y)
            if lastRowStr[distressX] == "#":
                #nextRowStr = findScannedPositions(sensors, minX, maxX, y+1)
                nextRowStr = createRow(minX, maxX, y+1, sensors)
                if nextRowStr[distressX] == "#":
                    return distressX,y

        lastRowStr = rowStr

    return 0,y


#
# Main
#
def main():

    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: " + sys.argv[0] + " inputfile row");
        return
    filename = args[0]
    row = int(args[1])
    print("Input File:", filename)
    print("Check Row: ", row)
    print()

    # Load data
    sensors = loadData(filename)
    print(" Sensors Read: ", len(sensors))
    print()
    printLines(sensors)
    minX = min([sensor.minX for sensor in sensors])
    maxX = max([sensor.maxX for sensor in sensors])
    minY = min([sensor.minY for sensor in sensors])
    maxY = max([sensor.maxY for sensor in sensors])
    #printGridOld(minX, maxX, minY, maxY, sensors)
    #printGrid(minX, maxX, minY, maxY, sensors)

    # Do Part 1 work
    print()
    answer = countNoBeaconRow(sensors, minX, maxX, row)
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    searchMinX = max(minX,0)
    searchMaxX = min(maxX,4000000)
    searchMinY = max(minY,0)
    searchMaxY = min(maxY,4000000)
    #printGrid(searchMinX, searchMaxX, searchMinY, searchMaxY, sensors)
    print()
    distressX, distressY = findDistressBeacon(sensors, searchMinX, searchMaxX, searchMinY, searchMaxY)
    print("x=", distressX, "y=", distressY)
    answer = distressX * 4000000 + distressY
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    start = time.perf_counter()
    now = datetime.now()
    print("Started at:", now.strftime("%Y-%m-%d %H:%M:%S"))
    main()
    end = time.perf_counter()
    elapsedTime = (end - start) * 10**6
    print(f"Elapsed time: {elapsedTime:.03f} micro secs.")
    now = datetime.now()
    print("Ended at:", now.strftime("%Y-%m-%d %H:%M:%S"))

