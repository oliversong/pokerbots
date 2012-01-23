from pokereval import PokerEval
from Enums import *
import pocketlookup

ITERATIONS = 10000

class Strategy:
    def __init__(self):
        self.pokereval = PokerEval()
        self.handRank = None

    def evaluateOdds(self, game):
        self.evaluatePocketCards(game)
        self.evalHand(game)
        #raise NotImplementedError("evaluateOdds not implemented in subclass")

    def getMove(self, game, archive):
        raise NotImplementedError("getMove not implemented in subclass")

    def evaluatePocketCards(self, game):
        self.handRank = pocketlookup.evalPocket(game.holeCard1, game.holeCard2)

    def evalHand(self, game):
        hand = [game.holeCard1.stringValue, game.holeCard2.stringValue]

        ev = self.pokereval.poker_eval(game="holdem",
                                       pockets = [hand,[255,255],[255,255]],
                                       dead=[],
                                       board=game.boardCards,
                                       iterations = ITERATIONS)['eval'][0]['ev']
#        print "HAND", hand, "BOARD", board, "EV", ev

        return ev

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

    #Bet or raise the minimum amount, or times some multiplier
    def pushMin(self, game, m=1):
        move = "CALL"
        if "BET" in [la[0] for la in game.legalActions]:
            move = "BET"+":"+str(int(min(self.get_allIn(b),int(la[1])*m)))
        elif "RAISE" in [la[0] for la in game.legalActions]:
            move= "RAISE"+":"+str(int(min(self.get_allIn(b),int(la[1])*m)))

##        print "PUSH MIN MOVE:", move
        return move

    ##If can check, then check.  Otherwise call up to m
    def maxRisk(self, game, m):
        if "CHECK" in [la[0] for la in game.legalActions]:
            return "CHECK"
        if game.lastBet <= m:
            return "CALL"
        return "FOLD"
