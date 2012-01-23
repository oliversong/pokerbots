from Strategy import *
from Enums import *

class LagRuleBotStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):

        ev = self.evalHand(game)

        if game.street()==PREFLOP:
            print "PREFLOP"
            if ev>400:
                return self.pushMin(game,3)
            elif ev>250:
                return self.pushMin(game)
            else:
                return self.maxRisk(game,2)
        elif game.street()==FLOP:
            print "FLOP"
            if ev>500:
                return self.pushMin(game,3)
            elif ev>350:
                return self.pushMin(game)
            else:
                return self.maxRisk(game,2)

        elif game.street()==TURN:
            print "TURN"
            if ev>600:
                return self.pushMin(game,3)
            elif ev>450:
                return self.pushMin(game)
            else:
                return self.maxRisk(game,2)
        elif game.street()==RIVER:
            print "RIVER"
            if ev>750:
                return self.pushMin(game,3)
            elif ev>550:
                return self.pushMin(game)
            else:
                return self.maxRisk(game,2)

        return "FOLD"
