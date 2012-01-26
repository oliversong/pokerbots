from Strategy import *
from Enums import *

class FoldBotStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):

        ev = self.evalHand(game)

        if game.street==PREFLOP:
            if ev > 350:
                if "RAISE" in [la[0] for la in game.legalActions]:
                    return "RAISE:200"
                if "BET" in [la[0] for la in game.legalActions]:
                    return "BET:200"
                return "CALL"
            else:
                return "CHECK"
        else:
            return "CHECK"
