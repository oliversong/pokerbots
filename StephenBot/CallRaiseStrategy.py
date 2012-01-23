from Strategy import *
from Enums import *

class CallRaiseStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):

        ev = self.evalHand(game)

        if game.street()==PREFLOP:
            return "CALL"
#            print "PREFLOP"
#            if ev>250:
#                return self.pushMin(game)
        elif game.street()==FLOP:
            return "CALL"
#            print "FLOP"
#            if ev>500:
#                return self.pushMin(game,3)
#            elif ev>350:
#                return self.pushMin(game)
#            else:
#                return self.maxRisk(game,2)

        elif game.street()==TURN:
            return "CALL"
#            print "TURN"
#            if ev>600:
#                return self.pushMin(game,3)
#            elif ev>450:
#                return self.pushMin(game)
#            else:
#                return self.maxRisk(game,2)
        elif game.street()==RIVER:
            return self.pushMin(game)
#            print "RIVER"
#            if ev>750:
#                return self.pushMin(game,3)
#            elif ev>550:
#                return self.pushMin(game)
#            else:
#                return self.maxRisk(game,2)

        return "FOLD"
