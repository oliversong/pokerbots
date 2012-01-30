from pokereval import PokerEval
from Enums import *
from Move import *
import TwoPocketLookup
import ThreePocketLookup

ITERATIONS = 10000

class Strategy:
    def __init__(self):
        self.pokereval = PokerEval()
        self.handRank = None

    def evaluateOdds(self, game):
        self.evaluatePocketCards3(game)
        self.evalHand(game)
        #raise NotImplementedError("evaluateOdds not implemented in subclass")

    def getMove(self, game, archive):
        raise NotImplementedError("getMove not implemented in subclass")

    def evaluatePocketCards2(self, game):
        return TwoPocketLookup.evalPocket(game.holeCard1, game.holeCard2)

    def evaluatePocketCards3(self, game):
        return ThreePocketLookup.evalPocket(game.holeCard1, game.holeCard2)

    def evalHand(self, game):
        hand = [game.holeCard1.stringValue, game.holeCard2.stringValue]
        if game.street==PREFLOP:
            if game.activePlayers == 2:
                ev = self.evaluatePocketCards2(game)
            else:
                ev = self.evaluatePocketCards3(game)
        else:
            if game.activePlayers == 3:
                pockets = [hand,[255,255],[255,255]]
            elif game.activePlayers == 2:
                pockets = [hand,[255,255]]
            else:
                # shouldn't get here, but just in case
                print "Only 1 active player! EV is 1"
                return 1000

            ev = self.pokereval.poker_eval(game="holdem",
                                           pockets = pockets,
                                           dead=[],
                                           board=game.boardCards,
                                           iterations = ITERATIONS)['eval'][0]['ev']
#        print "HAND", hand, "BOARD", board, "EV", ev

        return ev

    #Bet or raise the minimum amount, or times some multiplier
    # If min raise amount is to raise to 4, multiplier of 3 says to raise to
    # 3*4=12
    def pushMin(self, game, m=1):
        move = Move(CALL)
        for la in game.legalActions:
            if la[0] == "BET":
                return Move(BET, min(game.me.getAllIn(),int(la[1])*m))
            if la[0] == "RAISE":
                return Move(RAISE, min(game.me.getAllIn(),int(la[1])*m))

##        print "PUSH MIN MOVE:", move
        return move

    ##If can check, then check.  Otherwise call up to m
    def maxRisk(self, game, m):
        if "CHECK" in [la[0] for la in game.legalActions]:
            return Move(CHECK)
        if game.lastBet <= m:
            return Move(CALL)
        return Move(FOLD)
