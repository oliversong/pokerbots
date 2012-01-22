from Strategy import *
from Enums import *

class BasicEVStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):
        raiseAmt = 10

        move = "CHECK"


        ev = self.evalHand(b, game.boardCards)
        if ev>300:
            if "BET" in [la[0] for la in game.legalActions]:
                return la[0]+":"+la[1]
            elif "RAISE" in [la[0] for la in game.legalActions]:
                return la[0]+":"+la[1]





##        if move in [la[0] for la in game.legalActions] or move in ["BET","RAISE"]
##            if move == "RAISE" or "BET":
##                return move+str(raiseAmt)
##            else:
##                return move

        return "FOLD"
