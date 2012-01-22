from pokereval import PokerEval
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
    def pushMin(self, b, m=1):
        if "BET" in [la[0] for la in b.game.legalActions]:
            return "BET"+":"+str(int(la[1])*m)
        elif "RAISE" in [la[0] for la in b.game.legalActions]:
            return "RAISE"+":"+str(int(la[1])*m)
        return "CHECK" #CHECK LOGIC FOR THIS FUCNTION, SHOULD NEVER GET HERE

    ##If can check, then check.  Otherwise call up to m
    def maxRisk(self, b, m):
        if "CHECK" in [la[0] for la in b.game.legalActions]:
            return "CHECK"
        if b.game.lastBet <= m:
            return "CALL"
        return "FOLD"
