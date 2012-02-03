from Card import *
from MatchHistory import *
import random

class Participant():
    def __init__(self, name=""):
        self.name = name
        self.archive = MatchHistory(name)
        self.newGame()

    def newGame(self):
        self.bankroll = 0
        self.numBets = [0,0,0,0]            #how many times they Bet or Raise on each street
        self.amountContributed = [0,0,0,0]  #how much they contribute to pot
        self.amountBetRaise = [0,0,0,0]     #how much they contribute only on bet or raise
        self.archive.reset()
        self.aggFreq = [0,0,0,0]
        self.avgChips = [0,0,0,0]
        self.avgRaiseAmt = [0,0,0,0]
        self.numArrivalsAtStreet = [0,0,0,0]
        self.percentArrivals = [0,0,0,0]
        self.newHand()

    def newHand(self):
        # position: 0=dealer, 1=sb, 2=bb
        self.position = None
        self.stack = 200
        self.active = 1
        self.pip = 0
        self.totalPot = 0 #the pot + pips they saw when they last acted

        self.holeCard1 = None
        self.holeCard2 = None
        self.lastActions = []

        self.handRange = [(255,255)]

        self.aggFreqChanged = False

    def isAllIn(self):
        return self.stack == 0

    # Return amount needed to raise/bet all in
    def getAllIn(self):
        return int(self.stack + self.pip)

    def isLAP(self, game):
        numBets = self.numBets[game.street]
        handsAtStreet = game.numArrivalsAtStreet[game.street]
        x = numBets/float(handsAtStreet)
        if game.street == RIVER:
            return x < 0.15
        amountBetRaise = self.amountBetRaise[game.street]
        numStreetsSeen = self.numArrivalsAtStreet[game.street]
        if numStreetsSeen == 0.0:
            return False
        y = amountBetRaise/float(numStreetsSeen)
        if game.street == PREFLOP:
            return amountBetRaise/game.handID >= (12.0*x - 3.2)/0.1
        elif game.street == FLOP:
            return y >= (45.0*x - 10.25)/0.2
        elif game.street == TURN:
            return y >= (50.0*x - 7.0)/0.2
