from Strategy import *
from Enums import *

class LooseAgressiveStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def evaluateOdds(self, b):
        self.evaluatePocketCards(b)
        self.evalHand(b, b.game.boardCards)

    def getMove(self, b):
        raiseAmt = 10

        move = "CHECK"

        if b.game.street()==PREFLOP:
            print "PREFLOP"
            if b.game.position == 0: #DEALER
                if self.handRank > 655359:
                    move = "RAISE"
                elif self.handRank < 393216:
                    move = "FOLD"
                else: move = "CALL"
            elif b.game.position == 1: #small blind
                if self.handRank < 393216:
                    move = "FOLD"
                else:
                    move = "CALL"
            elif b.game.position == 2:
                if "RAISE" in [last[0] for last in b.game.lastActions]:
                    move = "FOLD"
                else:
                    move = "CHECK"

            raiseAmt = (3+1) * b.game.bigB
        elif b.game.street()==FLOP:
            print "FLOP"

            if self.handRank > 786431:
                move = "RAISE"
            move = "BET"
            raiseAmt = int(0.75 * b.game.potSize)
        elif b.game.street() == TURN:
            print "TURN"
            raiseAmt = 0
        elif b.game.street() == RIVER:
            print "RIVER"
            raiseAmt = 0


        if move in [la[0] for la in b.game.legalActions]:
            if move == "RAISE":
                return 'RAISE:'+str(raiseAmt)#str(3*b.game.bigB)
            elif move == "BET":
                return 'BET:'+str(raiseAmt)
            else:
                return move

        return "FOLD"
