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
                print "TWO PLAYER UNKNOWN OPP EV: ", ev
                #determine which player is still in
                if game.leftOpp.active == 1:
                    p = game.leftOpp
                else:
                    p = game.rightOpp
                #get their range of hands
                if p.name in oppEvs.keys():
                    pEV = oppEvs[p.name]
                    if pEV[0] != -1:
                        p.handRange = reduce(lambda x,y:x+y, TwoPocketLookup.lookupvalue[max([int(pEV[0]-pEV[1]),0]):min([int(pEV[0]+pEV[1]+1),1000])])
                        if len(p.handRange) == 0:
                            p.handRange = [(255,255)]
                        wins = 0
                        iters = ITERATIONS/len(p.handRange)
                        num_hands = 0
                        for h in p.handRange:
                            ev = self.pokereval.poker_eval(game="holdem",pockets=[hand,list(h)],dead=[],board=game.boardCards,iterations=iters)
                            wins += ev['eval'][0]['winhi']+ev['eval'][0]['tiehi']/2.0
                            num_hands+=1
                        ev = 1000 * wins/float(num_hands*iters)
                        print "TWO PLAYER EDUCATED EV:", ev

            else: #3 active players
                ev = self.evaluatePocketCards3(game)
                print "THREE PLAYER UNKNOWN OPP EV: ", ev
                game.leftOpp.handRange = [(255,255)]
                game.rightOpp.handRange = [(255,255)]
                if game.leftOpp.name in oppEvs.keys():
                    pEV = oppEvs[game.leftOpp.name]
                    if pEV[0] != -1:
                        game.leftOpp.handRange = reduce(lambda x,y:x+y, ThreePocketLookup.lookupvalue[max([int(pEV[0]-pEV[1]),0]):min([int(pEV[0]+pEV[1]+1),1000])])
                if game.rightOpp.name in oppEvs.keys():
                    pEV = oppEvs[game.rightOpp.name]
                    if pEV[0] != -1:
                        game.rightOpp.handRange = reduce(lambda x,y:x+y, ThreePocketLookup.lookupvalue[max([int(pEV[0]-pEV[1]),0]):min([int(pEV[0]+pEV[1]+1),1000])])
                if game.leftOpp.handRange !=[(255,255)] or game.rightOpp.handRange !=[(255,255)]:
                    wins = 0
                    samples = 3000
                    num_hands = 0
                    iters  = ITERATIONS/samples
                    for i in range(samples):
                        p1 = list(random.choice(game.leftOpp.handRange))
                        p2 = list(random.choice(game.rightOpp.handRange))
                        pockets = [hand,p1,p2]
                        ev = self.pokereval.poker_eval(game="holdem",pockets=pockets,dead=[],board=game.boardCards,iterations=iters)
                        wins += ev['eval'][0]['winhi'] + ev['eval'][0]['tiehi']/2.0
                        num_hands += 1
                    ev = 1000 * wins/float(num_hands*iters)
                    print "THREE PLAYER EDUCATED EV: ", ev

        else: #post-flop
            if game.activePlayers == 3:
#                wins = 0
#                wins1 = 0
#                wins2 = 0
#                samples = 3000
#                num_hands = 0
#                num_hands1 = 0
#                num_hands2 = 0
#                iters = ITERATIONS/samples
#                for i in range(samples):
#                    #get random pockets from both players
#                    p1 = list(game.leftOpp.handRange[random.randrange(len(game.leftOpp.handRange))])
#                    p2 = list(game.rightOpp.handRange[random.randrange(len(game.rightOpp.handRange))])
#                    pockets = [hand,p1,p2]
#                    ev = self.pokereval.poker_eval(game="holdem",pockets=pockets,dead=[],board=game.boardCards,iterations=iters)
#                    tempWins1 = ev['eval'][1]['winhi'] + ev['eval'][1]['tiehi']/2.0
#                    tempWins2 = ev['eval'][2]['winhi'] + ev['eval'][2]['tiehi']/2.0
#                    tempEV1 = 1000*tempWins1/iters
#                    tempEV2 = 1000*tempWins2/iters
#                    #check if opponent calculated evs are within their predicted evs by the archive
#                    if game.leftOpp.name in oppEvs.keys():
#                        if tempEV1 > (oppEvs[game.leftOpp.name][0] - oppEvs[game.leftOpp.name][1]) and tempEV1 < (oppEvs[game.leftOpp.name][0] +  oppEvs[game.leftOpp.name][1]):
#                            wins1 += tempWins1
#                            num_hands1 += 1
#                    else:
#                        wins1 += tempWins1
#                        num_hands1 += 1
#                    if game.rightOpp.name in oppEvs.keys():
#                        if tempEV2 > (oppEvs[game.rightOpp.name][0] - oppEvs[game.rightOpp.name][1]) and tempEV2 < (oppEvs[game.rightOpp.name][0] +  oppEvs[game.rightOpp.name][1]):
#                            wins2 += tempWins2
#                            num_hands2 += 1
#                    else:
#                        wins2 += tempWins2
#                        num_hands2 += 1
#                    wins += ev['eval'][0]['winhi'] + ev['eval'][0]['tiehi']/2.0
#                    num_hands += 1
#                ev = 1000*wins/float(num_hands*iters)
#                if num_hands1 > 0:
#                    ev1 = 1000*wins1/float(num_hands1*iters)
#                else:
#                    ev1 = -1
#                if num_hands2 >0:
#                    ev2 = 1000*wins2/float(num_hands2*iters)
#                else:
#                    ev2 = -1
#
#                ###unused except for printing
#                naiveEV = self.pokereval.poker_eval(game="holdem",pockets=[hand,[255,255],[255,255]],dead=[],board=game.boardCards,iterations = ITERATIONS)
#                naiveEV = 1000*(naiveEV['eval'][0]['winhi'] + naiveEV['eval'][0]['tiehi']/2.0)/float(ITERATIONS)
#                print "OPPEV KEYS:", oppEvs.keys(), "left:", game.leftOpp.name, "right", game.rightOpp.name
#                if game.leftOpp.name in oppEvs.keys():
#                    LEV = oppEvs[game.leftOpp.name]
#                else:
#                    LEV = -1
#                if game.rightOpp.name in oppEvs.keys():
#                    REV = oppEvs[game.rightOpp.name]
#                else:
#                    REV = -1
#                ###
#
#
#                print "THREE PLAYERS:"
#                print "My naive ev:", naiveEV, " educated ev:", ev
#                print game.leftOpp.name, " ev:", LEV, " educated ev:", ev1
#                print game.rightOpp.name, " ev:", REV, " educated ev:", ev2


                pockets = [hand,[255,255],[255,255]]
            elif game.activePlayers == 2:
#                if game.leftOpp.active == 1:
#                    p = game.leftOpp
#                else:
#                    p = game.rightOpp
#
##                if p.handRange != [(255,255)]:
#                    wins = 0
#                    wins1 = 0
#                    samples = 1000
#                    num_hands = 0
#                    num_hands1 = 0
#                    iters = ITERATIONS/samples
#                    for i in range(samples):
#                        if len(p.handRange)>1:
#                            p1 = list(p.handRange[random.randrange(len(p.handRange))])
#                            pockets = [[255,255],p1]
#                            ev = self.pokereval.poker_eval(game="holdem",pockets=pockets,dead=[],board=game.boardCards,iterations=iters)
#                            tempWins1 = ev['eval'][1]['winhi'] + ev['eval'][1]['tiehi']/2.0
#                            tempEV1 = 1000 * tempWins1/float(iters)
#                            #check if those possible cards in hand range give an EV that is in range we expect from history
#                            if p.name in oppEvs.keys():
#                                if oppEvs[p.name][0] != -1:
#                                    if tempEV1 > (oppEvs[p.name][0] - oppEvs[p.name][1]) and tempEV1 < (oppEvs[p.name][0] +  oppEvs[p.name][1]):
#                                        wins1 += tempWins1
#                                        num_hands1 += 1
#                            else:
#                                wins1 += tempWins1
#                                num_hands1 += 1
#                            print "REMOVING ELEMNT", p1
#                            p.handRange.remove((p1[0],p1[1]))
#                            #update our EV
#                            pockets = [hand, p1]
#                            ev = self.pokereval.poker_eval(game="holdem",pockets=pockets,dead=[],board=game.boardCards,iterations=iters)
#                            wins += ev['eval'][0]['winhi'] + ev['eval'][0]['tiehi']/2.0
#                            num_hands += 1
#                    ev = 1000*wins/float(num_hands*iters)
#                    if num_hands1 > 0:
#                        ev1 = 1000*wins1/float(num_hands1*iters)
#                    else:
#                        ev1 = -1
##
#                    ###only used in printing
#                    naiveEV = self.pokereval.poker_eval(game="holdem",pockets=[hand,[255,255]],dead=[],board=game.boardCards,iterations = ITERATIONS)
#                    naiveEV = 1000*(naiveEV['eval'][0]['winhi'] + naiveEV['eval'][0]['tiehi']/2.0)/float(ITERATIONS)
#                    if p.name in oppEvs.keys():
#                        PEV = oppEvs[p.name]
#                    else:
#                        PEV = -1
#
#                    print "TWO PLAYERS:"
#                    print "my naive ev:", naiveEV, " educated ev:", ev
#                    print p.name, " ev:", PEV, " educated ev:", ev1
#                    print "gameboard", game.boardCards
#
#                else:
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
