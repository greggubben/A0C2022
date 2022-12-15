#
# Adavent of Code Template
#
import sys
import copy
from math import prod

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
#Class to hold monkey info
#
class Monkey:

    def __init__(self, num, items, operation, testDiv, testTrue, testFalse):

        self.number = int(num)
        self.items = [int(i) for i in items]
        self.operation = operation
        self.testDiv = int(testDiv)
        self.testTrueMonkey = int(testTrue)
        self.testFalseMonkey = int(testFalse)

    def __str__(self):

        monkeyString  = f"Monkey {self.number}:\n"
        monkeyString += f"  Items: {', '.join(str(i) for i in self.items)}:\n"
        monkeyString += f"  Operation: new = {self.operation}:\n"
        monkeyString += f"  Test: divisible by {self.testDiv}:\n"
        monkeyString += f"    If true: throw to monkey {self.testTrueMonkey}:\n"
        monkeyString += f"    If false: throw to monkey {self.testFalseMonkey}:\n"

        return monkeyString


#
# Load the file into a data array
#
def loadData(filename):

    lines = []
    monkeys = []

    f = open(filename)
    monkeyNum = ""
    monkeyItems = []
    monkeyOper = ""
    monkeyTest = ""
    monkeyTrue = ""
    monkeyFalse = ""
    for line in f:
        line = line.strip()
        lines.append(line)
        if line == "":
            monkeys.append(Monkey(monkeyNum, monkeyItems, monkeyOper, monkeyTest, monkeyTrue, monkeyFalse))
            #print(monkeys[-1])
            monkeyNum = ""
            monkeyItems = []
            monkeyOper = ""
            monkeyTest = ""
            monkeyTrue = ""
            monkeyFalse = ""
        elif line.startswith("Monkey"):
            parts = line.split(" ")
            parts = parts[1].split(":")
            monkeyNum = parts[0]
        elif line.startswith("Starting items:"):
            parts = line.split(":")
            monkeyItems = parts[1].split(",")
        elif line.startswith("Operation:"):
            parts = line.split("=")
            monkeyOper = parts[1]
        elif line.startswith("Test:"):
            parts = line.split(" ")
            monkeyTest = parts[-1]
        elif line.startswith("If true:"):
            parts = line.split(" ")
            monkeyTrue = parts[-1]
        elif line.startswith("If false:"):
            parts = line.split(" ")
            monkeyFalse = parts[-1]
        else:
            print("bad input", line)

    monkeys.append(Monkey(monkeyNum, monkeyItems, monkeyOper, monkeyTest, monkeyTrue, monkeyFalse))
    #print(monkeys[-1])
    f.close()

    return monkeys


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


#
# Print the monkey items
#
def printMonkeyItems(monkeys):

    for monkey in monkeys:
        print(f"Monkey {monkey.number}: {', '.join(str(item) for item in monkey.items)}")


#
# Play keep away following the rules
#
def keepAway(monkeys, rounds, relief):

    monkeyInspections = [0 for m in monkeys]

    for r in range(0,rounds):
        for monkey in monkeys:
            #print(f"Monkey {monkey.number}:")
            for item in monkey.items:
                monkeyInspections[monkey.number] += 1
                #print(f"  Monkey inspects an item with a worry level of {item}.")
                old = item
                new = int(eval(monkey.operation))
                #print(f"    Worry level is '{monkey.operation}' to {new}.")
                new = int(eval(relief))
                #print(f"    Monkey gets bored with item. Worry level is divided by {relief} to {new}.")
                newMonkeyNum = monkey.testTrueMonkey
                if new % monkey.testDiv == 0:
                    #print(f"    Current worry level is divisible by {monkey.testDiv}.")
                    newMonkeyNum = monkey.testTrueMonkey
                else:
                    #print(f"    Current worry level is not divisible by {monkey.testDiv}.")
                    newMonkeyNum = monkey.testFalseMonkey
                #print(f"    Item with worry level {new} is thrown to monkey {newMonkeyNum}.")
                monkeys[newMonkeyNum].items.append(new)

            monkey.items = []
            #printMonkeyItems(monkeys)


        if r+1 in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:
            print()
            print(f"== After round {r+1} ==")
            print(monkeyInspections)

    return monkeyInspections


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
    monkeys = loadData(filename)
    print(" Monkeys Read: ", len(monkeys))
    print()
    printLines(monkeys)

    # Do Part 1 work
    print()
    monkeys1 = copy.deepcopy(monkeys)
    monkeyInspections = keepAway(monkeys1, 20, "new / 3")
    print(monkeyInspections)
    monkeyInspections.sort()
    answer = monkeyInspections[-1] * monkeyInspections[-2]
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    monkeys2 = copy.deepcopy(monkeys)
    reliefNum = prod(monkey.testDiv for monkey in monkeys2)
    relief = "new % " + str(reliefNum)
    print(relief)
    monkeyInspections = keepAway(monkeys2, 10000, relief)
    print(monkeyInspections)
    monkeyInspections.sort()
    answer = monkeyInspections[-1] * monkeyInspections[-2]
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
