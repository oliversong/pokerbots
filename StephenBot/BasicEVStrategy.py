from Strategy import *
from Enums import *
from Move import *

class BasicEVStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):
        ev = self.evalHand(game)
        if ev>300:
            if "BET" in [la[0] for la in game.legalActions]:
                return Move(BET,int(la[1]))
            elif "RAISE" in [la[0] for la in game.legalActions]:
                return Move(RAISE, int(la[1]))

        return Move(FOLD)
