from pokereval import PokerEval
from pocketlookup import *
from Enums import *

ITERATIONS = 10000

class Strategy:
    def __init__(self):
        self.pokereval = PokerEval()
        self.handRank = None
        self.index1 = 0
        self.index2 = 0

    def evaluateOdds(self, b):
        raise NotImplementedError("evaluateOdds not implemented in subclass")
    def getMove(self, b):
        raise NotImplementedError("getMove not implemented in subclass")
    
    
    def evaluatePocketCards(self, b):
        v1 = b.holeCard1.value - 2
        v2 = b.holeCard2.value - 2

        self.index1 = min(v1,v2)
        self.index2 = max(v1,v2) - self.index1

        suited = 1  #off suit hole cards
        if b.holeCard2.suit == b.holeCard1.suit:
            suited = 0  #suited

        self.handRank = lookuphand[self.index1][self.index2][suited]

    def evalHand(self, b, board):
#        print "BOARDCARDS", board
        hand = [b.holeCard1.stringValue, b.holeCard2.stringValue]

        ev = self.pokereval.poker_eval(game="holdem", 
                                       pockets = [hand,[255,255],[255,255]],
                                       dead=[], 
                                       board=board,
                                       iterations = ITERATIONS)['eval'][0]['ev']
#        print "HAND", hand, "BOARD", board, "EV", ev

        return ev

    #Bet or raise the minimum amount, or times some multiplier def pushMin(self, b, m=1):
 #   def pushMin(self, b, m=1):
 #       if "BET" in [la[0] for la in b.state.legalActions]:
 #           return "BET"+":"+str(int(la[1])*m)
 #       elif "RAISE" in [la[0] for la in b.state.legalActions]:
 #           return "RAISE"+":"+str(int(la[1])*m)
 #       return "CHECK" #CHECK LOGIC FOR THIS FUCNTION, SHOULD NEVER GET HERE

    ##If can check, then check.  Otherwise call up to m
#    def maxRisk(self, b, m):
#        if "CHECK" in [la[0] for la in b.state.legalActions]:
#            return "CHECK"
#        if b.state.lastBet <= m:
#            return "CALL"
#        return "FOLD"

    def get_allIn(self,b):
        st = -3
        bets = [0,0,0,0]
        prevBet = 0
        allinbet = 200
        for acts in b.state.hand.actions:
            if acts.type == DEAL:
                st+=1
                prevBet = 0
            elif acts.player != b.state.rightOpp and acts.player!= b.state.leftOpp and acts.type in [CALL, BET, RAISE, POST]: #Want to say acts.player == b.state.myName what is the field name for our name?
                if acts.type == CALL:
                    bets[st] = prevBet
                elif acts.type == POST:
                    bets[0] = acts.amount
                else:
                    bets[st] = acts.amount
                    
            if acts.type in [BET, RAISE, POST]:
                preBet = acts.amount

        if st>0:
            for i in range(st-1):
                allinbet -= bets[i]

        return allinbet

    #Bet or raise the minimum amount, or times some multiplier def pushMin(self, b, m=1):
    def pushMin(self, b, m=1):
        #self.numPushMin += 1
#        print "PUSH MIN:", self.numPushMin
        if "BET" in [la[0] for la in b.state.legalActions]:
            move = "BET"+":"+str(int(min(self.get_allIn(b),int(la[1])*m)))
        elif "RAISE" in [la[0] for la in b.state.legalActions]:
            move= "RAISE"+":"+str(int(min(self.get_allIn(b),int(la[1])*m)))
        else:
            move = "CALL"

	
        print "PUSH MIN MOVE:", move
        return move #CHECK LOGIC FOR THIS FUCNTION, SHOULD NEVER GET HERE

    ##If can check, then check. Otherwise call up to m
    def maxRisk(self, b, m):
        if "CHECK" in [la[0] for la in b.state.legalActions]:
            return "CHECK"
        if b.state.lastBet <= m:
            return "CALL"
        return "FOLD"

