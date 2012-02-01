from Card import *

class Participant():
    def __init__(self, name=""):
        self.name = name
        self.newGame()

    def newGame(self):
        self.bankroll = 0
        self.numBets = [0,0,0,0]            #how many times they Bet or Raise on each street
        self.amountContributed = [0,0,0,0]  #how much they contribute to pot
        self.amountBetRaise = [0,0,0,0]     #how much they contribute only on bet or raise
        self.newHand()

        self.aggFreq = [0,0,0,0]
        self.avgChips = [0,0,0,0]
        self.avgBetRaiseChips = [0,0,0,0]

    def newHand(self):
        self.position = None
        self.stack = 200
        self.active = 1
        self.pip = 0

        self.holeCard1 = None
        self.holeCard2 = None
        self.lastActions = []

        self.aggFreqChanged = False

    def isAllIn(self):
        return self.stack == 0

    # Return amount needed to raise/bet all in
    def getAllIn(self):
        return int(self.stack + self.pip)
