from Strategy import *
from Enums import *
from Move import *

class LooseAgressiveStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):
        raiseAmt = 10

        move = Move(CHECK)

        if game.street==PREFLOP:
            print "PREFLOP"
            if game.position == 0: #DEALER
                if self.handRank > 655359:
                    move = Move(RAISE)
                elif self.handRank < 393216:
                    move = Move(FOLD)
                else: move = Move(CALL)
            elif game.position == 1: #small blind
                if self.handRank < 393216:
                    move = Move(FOLD)
                else:
                    move = Move(CALL)
            elif game.position == 2:
                if "RAISE" in [last[0] for last in game.lastActions]:
                    move = Move(FOLD)
                else:
                    move = Move(CHECK)

            raiseAmt = (3+1) * game.bigB
        elif game.street==FLOP:
            print "FLOP"

            if self.handRank > 786431:
                move = Move(RAISE)
            move = Move(BET)
            raiseAmt = int(0.75 * game.potSize)
        elif game.street == TURN:
            print "TURN"
            raiseAmt = 0
        elif game.street == RIVER:
            print "RIVER"
            raiseAmt = 0


        if move in [la[0] for la in game.legalActions]:
            if move == "RAISE":
                return Move(RAISE, raiseAmt)#str(3*game.bigB)
            elif move == "BET":
                return Move(BET, raiseAmt)
            else:
                return move

        return "FOLD"
