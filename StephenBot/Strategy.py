from pokereval import PokerEval
from pocketlookup import *

ITERATIONS = 10000

class Strategy:
    def __init__(self):
        self.pokereval = PokerEval()
        self.handRank = None

    def evaluateOdds(self, b):
        raise NotImplementedError("evaluateOdds not implemented in subclass")
    def getMove(self, b):
        raise NotImplementedError("getMove not implemented in subclass")
    
    
    def evaluatePocketCards(self, b):
        v1 = b.holeCard1.value - 2
        v2 = b.holeCard2.value - 2

        self.index1 = min(v1,v2)
        self.index2 = max(v1,v2) - self.index1

        suited = 1  #off suit hole cards
        if b.holeCard2.suit == b.holeCard1.suit:
            suited = 0  #suited

        self.handRank = lookuphand[self.index1][self.index2][suited]

    def evalHand(self, b, board):
        hand = [b.holeCard1.stringValue, b.holeCard2.stringValue]

        ev = self.pokereval.poker_eval(game="holdem", 
                                       pockets = [hand,[255,255],[255,255]],
                                       dead=[], 
                                       board=board,
                                       iterations = ITERATIONS)['eval'][0]['ev']
        print "HAND", hand, "BOARD", board, "EV", ev

        return ev

