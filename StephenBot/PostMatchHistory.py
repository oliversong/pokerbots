from math import *
from Action import *
from Hand import *
from Enums import *
from GameState import *
from ParseMatchHistory import *
from Card import *

import ThreePocketLookup
import TwoPocketLookup

from pokereval import PokerEval

class PostMatchHistory:
    def __init__(self):
        self.history = {}
        self.pokereval = PokerEval()

    def reset(self, game):
        self.history[game.leftOpp.name] = [{},{},{},{}]
        self.history[game.rightOpp.name] = [{},{},{},{}]
        for a in range(4): #[BET, CALL, CHECK, RAISE]
            for s in range(4): #streets
                self.history[game.leftOpp.name][s][a] = []
                self.history[game.rightOpp.name][s][a] = []

    def update(self, game):
        showStats = {}

        for player in [game.me, game.leftOpp, game.rightOpp]:
            showStats[player.name] = [[player.holeCard1, player.holeCard2], [0,0]]

        for player in showStats.keys():
            playerHand = showStats[player][0]
            ev2 = TwoPocketLookup.evalPocket(Card(playerHand[0]),
                                             Card(playerHand[1]))
            ev3 = ThreePocketLookup.evalPocket(Card(playerHand[0]),
                                               Card(playerHand[1]))
            showStats[player][1] = [ev2, ev3]

        street = 0
        activePlayers = 3
        b = [255]*5
        for action in game.hand.actions:
            if action.type == DEAL:
                street += 1
                if street == FLOP:
                    b[:3] = game.boardCards[:3]
                elif street==TURN: #TURN
                    b[:4] = game.boardCards[:4]
                elif street==RIVER: #RIVER
                    b = game.boardCards
                for player in showStats.keys():
                    playerHand = showStats[player][0]
                    #calculate ev3
                    pockets = [playerHand,[255,255],[255,255]]
                    ev3 = self.pokereval.poker_eval(game="holdem",
                                                    pockets=pockets,
                                                    dead=[],
                                                    board=b,
                                                    iterations=ITERATIONS)['eval'][0]['ev']
                    ev2 = self.pokereval.poker_eval(game="holdem",
                                                    pockets=pockets[:2],
                                                    dead=[],
                                                    board=b,
                                                    iterations=ITERATIONS)['eval'][0]['ev']
                    showStats[player][1] = [ev2,ev3]
            elif action.player in showStats.keys() and action.type != POST and action.type in game.hand.trackedActions:
                act = action.copy()
                act.ev = showStats[action.player][1]
                self.history[act.player][street][action.type].append(act)

    def printHistory(self):
        print "PRINTING HISTORY"
#        print self.history.keys()
        for p in self.history.keys():
            print "PLAYER",p
            for s in range(4):
                print "    STREET", s
                for a in self.history[p][s].keys():
                    print "        ACTION", ACTION_TYPES[a]
                    for i in range(len(self.history[p][s][a])):
                        act = self.history[p][s][a][i]
                        print "             [",
                        print "TYPE:", ACTION_TYPES[act.type],",",
                        print "PLAYER:", act.player,",",
                        print "AMOUNT:", act.amount,",",
                        print "POT AMOUNT:", act.potAmount,",",
                        print "BET AMOUNT:", act.betAmount,
                        print "EV:", act.ev, "]"

    def averageStrength(self, player, game, action, amountType):
        sum = 0
        sum2 = 0
        numMatches = 0
        std = 0

        amountDiffs = [] #list of action values [(action, actionAmount, abs(amount-actionAmount)

        #print self.history.keys() ##Need to comment out
        if action.type not in self.history[player][game.street].keys():
            print "ACTION TYPE IN AVERAGE STRENGTH", action.type
            return [-1,1000]
        actions = self.history[player][game.street][action.type]
        for a in actions:
            ev = a.ev[game.activePlayers-2]
            if amountType==POTAMOUNT:
                if a.potAmount==action.potAmount:
                    sum += ev
                    sum2 += ev*ev
                    numMatches += 1
                    mean = float(sum)/numMatches
                    std = sqrt((float(sum2)/numMatches) - (mean*mean))
                else:
                    amountDiffs += [(a, a.potAmount, abs(a.potAmount - action.potAmount))]
            elif amountType==BETAMOUNT:
                if a.betAmount==action.betAmount:
                    sum += ev
                    sum2 += ev*ev
                    numMatches += 1
                    mean = float(sum)/numMatches
                    std = sqrt((float(sum2)/numMatches) - (mean*mean))
                else:
                    amountDiffs += [(a, a.betAmount, abs(a.betAmount - action.betAmount))]
            else:
                if a.amount==action.amount:
                    sum += ev
                    numMatches += 1
                    sum2 += ev*ev
                    mean = float(sum)/numMatches
                    std = sqrt((float(sum2)/numMatches) - (mean*mean))
                else:
                    upperBound = action.amount + 2 + 0.10*action.amount
                    lowerBound = action.amount - 2 - 0.10*action.amount
                    #only use actions within a certain range to calculate average/std values
                    if a.amount <= upperBound and a.amount >= lowerBound:
                        amountDiffs += [(a, a.amount, abs(a.amount - action.amount))]

        if numMatches<3:
           #sort the amountDiffs by the difference in amount from the desired amount
            amountDiffs = sorted(amountDiffs, key=lambda x: x[2])
            minDiff = 0
            for amt in amountDiffs:
                ev = amt[0].ev[game.activePlayers-2]
                if amt[2] != minDiff:
                    minDiff = amt[2]
                    if numMatches>=3:
                        return [float(sum)/float(numMatches), std]
                sum += ev
                numMatches += 1
                sum2 += ev*ev
                mean = float(sum)/numMatches
                std = sqrt((float(sum2)/float(numMatches)) - (mean*mean))

            return [-1,1000]

        return [float(sum)/float(numMatches), std]
