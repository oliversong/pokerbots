from Strategy import *
from Enums import *

class LooseAgressiveStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)
        self.index1 = 0
        self.index2 = 0

    def evaluateOdds(self, b):
        self.evaluatePocketCards(b)
        self.evalHand(b, b.state.boardCards)

    def getMove(self, b):
        raiseAmt = 10
        
        move = "CHECK"

        if b.state.street()==PREFLOP:
            print "PREFLOP"
            if b.state.position == 0: #DEALER
                if self.handRank > 655359:
                    move = "RAISE"
                elif self.handRank < 393216:
                    move = "FOLD" 
                else: move = "CALL"
            elif b.state.position == 1: #small blind
                if self.handRank < 393216:
                    move = "FOLD"
                else:
                    move = "CALL"
            elif b.state.position == 2:
                if "RAISE" in [last[0] for last in b.state.lastActions]:
                    move = "FOLD"
                else:
                    move = "CHECK"

            raiseAmt = (3+1) * b.state.bigB
        elif b.state.street()==FLOP:
            print "FLOP"
            
            if self.handRank > 786431:
                move = "RAISE"
            move = "BET"
            raiseAmt = int(0.75 * b.state.potSize)
        elif b.state.street() == TURN:
            print "TURN"
            raiseAmt = 0
        elif b.state.street() == RIVER:
            print "RIVER"
            raiseAmt = 0


        if move in [la[0] for la in b.state.legalActions]:
            if move == "RAISE":
                return 'RAISE:'+str(raiseAmt)#str(3*b.state.bigB)
            elif move == "BET":
                return 'BET:'+str(raiseAmt)
            else:
                return move

        return "FOLD"



