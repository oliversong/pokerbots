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

    #Bet or raise the minimum amount, or times some multiplier
    # If min raise amount is to raise to 4, multiplier of 3 says to raise to
    # 3*4=12
    def pushMin(self, game, m=1):
        move = "CALL"
        for la in game.legalActions:
            if la[0] == "BET":
                return "BET:"+str(min(game.getAllIn(),int(la[1])*m))
            if la[0] == "RAISE":
                return "RAISE:"+str(min(game.getAllIn(),int(la[1])*m))

##        print "PUSH MIN MOVE:", move
        return move

    ##If can check, then check.  Otherwise call up to m
    def maxRisk(self, game, m):
        if "CHECK" in [la[0] for la in game.legalActions]:
            return "CHECK"
        if game.lastBet <= m:
            return "CALL"
        return "FOLD"
