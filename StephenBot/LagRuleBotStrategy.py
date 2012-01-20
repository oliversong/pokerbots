from Strategy import *
from Enums import *

class LagRuleBotStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def evaluateOdds(self, b):
        self.evaluatePocketCards(b)
        self.evalHand(b, b.state.boardCards)

    def getMove(self, b):

        ev = self.evalHand(b, b.state.boardCards)

        if b.state.street()==PREFLOP:
            print "PREFLOP"
            if ev>400:
                return self.pushMin(b,3)
            elif ev>250:
                return self.pushMin(b)
            else:
                return self.maxRisk(b,2)
        elif b.state.street()==FLOP:
            print "FLOP"
            if ev>500:
                return self.pushMin(b,3)
            elif ev>350:
                return self.pushMin(b)
            else:
                return self.maxRisk(b,2)

        elif b.state.street()==TURN:
            print "TURN"
            if ev>600:
                return self.pushMin(b,3)
            elif ev>450:
                return self.pushMin(b)
            else:
                return self.maxRisk(b,2)
        elif b.state.street()==RIVER:
            print "RIVER"
            if ev>750:
                return self.pushMin(b,3)
            elif ev>550:
                return self.pushMin(b)
            else:
                return self.maxRisk(b,2)

        return "FOLD"

