from Strategy import *
from Enums import *
from Move import *

class FoldBotStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):
        print "hahah"
        for la in game.legalActions:
            if la[0] == "BET":
                return Move(BET, 10)
            if la[0] == "RAISE":
                if game.street == PREFLOP:
                    return Move(RAISE, 10)
                return Move(FOLD)

        return Move(CHECK)
