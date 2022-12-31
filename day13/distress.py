#
# Adavent of Code Template
#
import sys
from enum import Enum

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

DEBUG = False

# only print if debugging
def debugPrint(s=""):
    if DEBUG:
        print(s)


#
# results of comparison values
Compare = Enum('Compare', ['LESS', 'SAME', 'GREATER'])


#
# Class to hold a Packet
#   include functions for special comparisons
#
class Packet:

    def __init__(self, valueStr):

        self.value = eval(valueStr)

    def __str__(self):
        return f"{self.value}"

    def __lt__(left, right):
        return compareValues(left.value, right.value) == Compare.LESS

    def __le__(left, right):
        return compareValues(left.value, right.value) in [Compare.LESS, Compare.SAME]

    def __eq__(left, right):
        return compareValues(left.value, right.value) == Compare.SAME

    def __ne__(left, right):
        return compareValues(left.value, right.value) != Compare.SAME

    def __ge__(left, right):
        return compareValues(left.value, right.value) in [Compare.GREATER, Compare.SAME]

    def __gt__(left, right):
        return compareValues(left.value, right.value) == Compare.GREATER


#
# Load the file into a data array
#
def loadData(filename):

    packetPairs = []
    packets = []

    f = open(filename)
    LoadingFirstValue = True
    for line in f:
        line = line.strip()
        if len(line) == 0:
            # end of packets
            packetPairs.append([firstValue, secondValue])
            LoadingFirstValue = True
        else:
            packet = Packet(line)
            packets.append(packet)
            if LoadingFirstValue:
                # Load the first value
                firstValue = packet
                LoadingFirstValue = False
            else:
                # Load the second value
                secondValue = packet

    packetPairs.append([firstValue, secondValue])

    f.close()

    return packetPairs, packets


#
# Print Array
#
def printPackets(packets):

    for packet in packets:
      print(packet)

#
# Print Array
#
def printPairs(packets):

    for packet in packets:
      print(packet[0], "vs", packet[1])


#
# Compare the packet values for the right order
#
def compareValues(left, right, indent=0):

    rightOrder = Compare.SAME
    debugPrint(f"{' ' * indent}- Compare {left} vs {right}")
    indent += 2

    if type(left) is list and type(right) is not list:
        # turn right into a list
        right = [right]
        debugPrint(f"{' ' * indent}- Mixed types; convert right to {right} and retry comparison")
        rightOrder = compareValues(left, right, indent)

    elif type(left) is not list and type(right) is list:
        # turn left into a list
        left = [left]
        debugPrint(f"{' ' * indent}- Mixed types; convert left to {left} and retry comparison")
        rightOrder = compareValues(left, right, indent)
    
    elif type(left) is list and type(right) is list:
        # loop through the lists
        leftLen = len(left)
        rightLen = len(right)
        valuesToCompare = min(leftLen, rightLen)
        for p in range(valuesToCompare):
            leftValue = left[p]
            rightValue = right[p]
            rightOrder = compareValues(leftValue, rightValue, indent)
            if rightOrder == Compare.SAME:
                continue
            else:
                break

        if rightOrder == Compare.SAME and leftLen != rightLen:
            if leftLen < rightLen:
                debugPrint(f"{' ' * indent}- Left side ran out of items, so inputs are {color.BOLD}in the right order{color.END}")
                rightOrder = Compare.LESS
            else:
                debugPrint(f"{' ' * indent}- Right side ran out of items, so inputs are {color.BOLD}not{color.END} in the right order")
                rightOrder = Compare.GREATER

    else:
        # Simple integers to compare
        if left == right:
            rightOrder = Compare.SAME
        elif left < right:
            debugPrint(f"{' ' * indent}- Left side is smaller, so inputs are {color.BOLD}in the right order{color.END}")
            rightOrder = Compare.LESS
        else:
            debugPrint(f"{' ' * indent}- Right side is smaller, so inputs are {color.BOLD}not{color.END} in the right order")
            rightOrder = Compare.GREATER

    return rightOrder


#
# Count the packets in the right order
#
def comparePackets(packets):

    rightOrderPairs = []
    pair = 0
    for packet in packets:
        pair += 1
        debugPrint(f"== Pair {pair} ==")

        #rightOrder = compareValues(packet[0], packet[1], 0)

        #if rightOrder == Compare.LESS:
        if packet[0] < packet[1]:
            rightOrderPairs.append(pair)

        debugPrint()

    return rightOrderPairs


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
    packetPairs, packets = loadData(filename)
    print(" Packets Read: ", len(packets))
    print(" Packets Pairs Read: ", len(packetPairs))
    print()
    printPairs(packetPairs)

    # Do Part 1 work
    print()
    rightOrderPairs = comparePackets(packetPairs)
    answer = sum(rightOrderPairs)
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    divider1 = Packet("[[2]]")
    divider2 = Packet("[[6]]")
    packets.append(divider1)
    packets.append(divider2)
    printPackets(packets)
    packets.sort()
    print("sorted")
    printPackets(packets)
    divider1Pos = packets.index(divider1) + 1
    divider2Pos = packets.index(divider2) + 1
    answer = divider1Pos * divider2Pos
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
