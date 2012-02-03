from pokereval import PokerEval
from Enums import *
from Move import *
import TwoPocketLookup
import ThreePocketLookup
import random

ITERATIONS = 10000

class Strategy:
    def __init__(self):
        self.pokereval = PokerEval()
        self.handRank = None

    def evaluateOdds(self, game):
        self.evaluatePocketCards3(game)
        self.evalHand(game)
        #raise NotImplementedError("evaluateOdds not implemented in subclass")

    def getMove(self, game):
        raise NotImplementedError("getMove not implemented in subclass")

    def evaluatePocketCards2(self, game):
        return TwoPocketLookup.evalPocket(game.holeCard1, game.holeCard2)

    def evaluatePocketCards3(self, game):
        return ThreePocketLookup.evalPocket(game.holeCard1, game.holeCard2)

    def evalHand(self, game, oppEvs = {}):
        hand = [game.holeCard1.stringValue, game.holeCard2.stringValue]
        if game.street==PREFLOP:
            if game.activePlayers == 2:
                ev = self.evaluatePocketCards2(game)
#                print "TWO PLAYER UNKNOWN OPP EV: ", ev
                #determine which player is still in
                if game.leftOpp.active == 1:
                    p = game.leftOpp
                else:
                    p = game.rightOpp
                #get their range of hands
                if p.name in oppEvs.keys():
                    pEV = oppEvs[p.name]
                    if pEV[0] != -1:
                        p.handRange = reduce(lambda x,y:x+y, TwoPocketLookup.lookupvalue[int(pEV[0]-pEV[1]):int(pEV[0]+pEV[1]+1)])
                        wins = 0
                        iters = ITERATIONS/len(p.handRange)
                        num_hands = 0
                        for h in p.handRange:
                            ev = self.pokereval.poker_eval(game="holdem",pockets=[hand,list(h)],dead=[],board=game.boardCards,iterations=iters)
                            wins += ev['eval'][0]['winhi']+ev['eval'][0]['tiehi']/2.0
                            num_hands+=1
                        ev = 1000 * wins/float(num_hands*iters)
#                        print "TWO PLAYER EDUCATED EV:", ev
                        
            else:
                ev = self.evaluatePocketCards3(game)
#                print "THREE PLAYER UNKNOWN OPP EV: ", ev
                lHands = [(255,255)]
                rHands = [(255,255)]
                if game.leftOpp.name in oppEvs.keys():
                    pEV = oppEvs[game.leftOpp.name]
                    if pEV[0] != -1:
                        lHands = reduce(lambda x,y:x+y, ThreePocketLookup.lookupvalue[int(pEV[0]-pEV[1]):int(pEV[0]+pEV[1]+1)])
                if game.rightOpp.name in oppEvs.keys():
                    pEV = oppEvs[game.rightOpp.name]
                    if pEV[0] != -1:
                        rHands = reduce(lambda x,y:x+y, ThreePocketLookup.lookupvalue[int(pEV[0]-pEV[1]):int(pEV[0]+pEV[1]+1)])
                if lHands !=[(255,255)]  or rHands!=[(255,255)]: 
                    wins = 0
                    allPairs = []
                    samples = 3000
                    num_hands = 0
                    iters  = ITERATIONS/samples
                    for i in range(samples):
                        p1 = list(lHands[random.randrange(len(lHands))])
                        p2 = list(rHands[random.randrange(len(rHands))])
                        pockets = [hand,p1,p2]
                        ev = self.pokereval.poker_eval(game="holdem",pockets=pockets,dead=[],board=game.boardCards,iterations=iters)
                        wins += ev['eval'][0]['winhi'] + ev['eval'][0]['tiehi']/2.0
                        num_hands += 1
                    ev = 1000 * wins/float(num_hands*iters)
#                    print "THREE PLAYER EDUCATED EV: ", ev
                
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

    def betPot(self, game, m):
        move = Move(CALL)
        amt = min(game.me.getAllIn(),m*(game.pot + game.leftOpp.pip + game.rightOpp.pip + game.me.pip))
        for la in game.legalActions:
            if la[0] == "BET":
                return Move(BET, amt)
            if la[0] == "RAISE":
                return Move(RAISE, amt)

##        print "PUSH MIN MOVE:", move
        return move
    def raiseBet(self, game, m):
        move = Move(CALL)
        highpip2 = sorted([game.me.pip, game.leftOpp.pip, game.rightOpp.pip])[1]
        amt = 3*(game.lastBet-highpip2)
        amt = max(game.pot, amt)
        amt = min(game.me.getAllIn(),m*amt)
        for la in game.legalActions:
            if la[0] == "RAISE":
                return Move(RAISE, amt)
        return move
