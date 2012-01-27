from Strategy import *
from Enums import *
from Move import *

class FoldBotStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):

        ev = self.evalHand(game)

        playEV = [650,500]

        if game.street==PREFLOP and ev > playEV[game.activePlayers-2]:
            if "RAISE" in [la[0] for la in game.legalActions]:
                return Move(RAISE, game.stackSize)
            if "BET" in [la[0] for la in game.legalActions]:
                return Move(BET, game.stackSize)
            return Move(CALL)
        return Move(CHECK)
