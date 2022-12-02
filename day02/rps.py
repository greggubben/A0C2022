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


number2Shape = { 1:"Rock", 2:"Paper", 3:"Sissors" }
win2String = { 0: "Loss", 3: "Draw", 6: "Win" }
win2Color = { 0: color.RED, 3: color.YELLOW, 6: color.GREEN }

#
# Strategy selections
#
class Strategy:
    input2Number = { "A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3 }
    outcome2Number = { "X": 0, "Y": 3, "Z": 6 }

    def __init__ (self, opp, me):
        self.oppChoiceStr = opp
        self.oppChoiceNum = self.input2Number[opp]
        self.myChoiceStr = me
        self.myChoiceNum = self.input2Number[me]
        self.outcome = self.outcome2Number[me]

    def __str__(self):
        return f"{color.CYAN}{self.oppChoiceStr} " + \
               f"{color.PURPLE}({self.oppChoiceNum}:{number2Shape[self.oppChoiceNum]:7})" + \
               f"{color.CYAN} -> Choice: " + \
               f"{color.YELLOW}{self.myChoiceStr} " + \
               f"{color.PURPLE}({self.myChoiceNum}:{number2Shape[self.myChoiceNum]:7})" + \
               f"{color.CYAN} | End: " + \
               f"{win2Color[self.outcome]}{self.outcome}:{win2String[self.outcome]:4}" + \
               f"{color.END}"


#
# Change the choice selection
#
def changeChoice(selection):
    win2Number = { 1: 2, 2: 3, 3: 1 }
    lose2Number = { 1: 3, 2: 1, 3: 2 }
    
    if selection.outcome == 0:
        # Lose
        selection.myChoiceNum = lose2Number[selection.oppChoiceNum]
    elif selection.outcome == 3:
        # Draw
        selection.myChoiceNum = selection.oppChoiceNum
    elif selection.outcome == 6:
        # Win
        selection.myChoiceNum = win2Number[selection.oppChoiceNum]



#
# Outcomes for Choices
#
class Outcome:
    win = { 1: 3, 2: 1, 3: 2 }

    def __init__ (self, choice):
        self.choice = choice
        if choice.oppChoiceNum == choice.myChoiceNum:
            # Draw
            self.outcome = 3
        elif self.win[choice.myChoiceNum] == choice.oppChoiceNum:
            # Win
            self.outcome = 6
        else:
            # Loss
            self.outcome = 0
        self.score = choice.myChoiceNum + self.outcome

    def __str__ (self):
        return f"{self.choice} " + \
               f"{color.CYAN} => Outcome: " + \
               f"{win2Color[self.outcome]}{self.outcome}:{win2String[self.outcome]:4} " + \
               f"Score = {self.score}" + \
               f"{color.END}"


#
# Load the file into a data array
#
def loadData(filename):

    strategies = []

    f = open(filename)
    for line in f:
        line = line.strip()
        opp, me = line.split(" ")
        strategies.append(Strategy(opp,me))

    f.close()

    return strategies


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


#
# Compute the wins of the strategy
#
def computeWins(strategy):

    wins = []

    for choice in strategy:
        wins.append(Outcome(choice))

    return wins


#
# Force the desired outcomes
#
def forceOutcomes(strategy):

    wins = []

    for choice in strategy:
        changeChoice(choice)
        wins.append(Outcome(choice))

    return wins


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
    strategy = loadData(filename)
    print(" Lines Read: ", len(strategy))
    print()
    printLines(strategy)

    # Do Part 1 work
    print()
    scores = computeWins(strategy)
    printLines(scores)
    answer = sum(s.score for s in scores)
    print()
    print("{}Part 1 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    scores2 = forceOutcomes(strategy)
    printLines(scores2)
    answer = sum(s.score for s in scores2)
    print()
    print("{}Part 2 Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
