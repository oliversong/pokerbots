from math import *
from Action import *
from Hand import *
from GameState import *
from Enums import *
import ThreePocketLookup
import TwoPocketLookup
from Card import *

from pokereval import PokerEval

class MatchHistory:
    def __init__(self):
        self.history = {}
        self.pokereval = PokerEval()
        self.showStats = {}

    def reset(self, game):
        #self.history[game.leftOpp.name] = [{},{},{},{}]
        for pname in [game.leftOpp.name, game.rightOpp.name]:
            if pname not in self.history.keys():
                self.history[pname] = [{},{},{},{}]
                for a in range(4):#[BET,CALL,CHECK,RAISE]:
                    for s in range(4):
                        self.history[pname][s][a] = []

    def update(self, game):
        self.showStats = {}

        for action in game.hand.actions:
            if action.type == SHOW and action.player in self.history.keys():
                self.showStats[action.player] = [[action.showCard1, action.showCard2],[0,0]]

        if len(self.showStats.keys()) > 0:
            self.computeNewEntries(game)

    def computeNewEntries(self, game):
        for player in self.showStats.keys():
            playerHand = self.showStats[player][0]
            ev2 = TwoPocketLookup.evalPocket(Card(playerHand[0]),Card(playerHand[1]))
            ev3 = ThreePocketLookup.evalPocket(Card(playerHand[0]),Card(playerHand[1]))
            self.showStats[player][1] = [ev2,ev3]

        street = 0
        b = [255]*5
        for action in game.hand.actions:
            if action.type == DEAL:
                street += 1
                if street==FLOP: #FLOP
                    b[:3] = game.boardCards[:3]
                elif street==TURN: #TURN
                    b[:4] = game.boardCards[:4]
                elif street==RIVER: #RIVER
                    b = game.boardCards
                for player in self.showStats.keys():
                    playerHand = self.showStats[player][0]
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
                    self.showStats[player][1] = [ev2,ev3]
            elif action.player in self.showStats.keys() and action.type != POST and action.type in game.hand.trackedActions:
                act = action.copy()
                act.ev = self.showStats[action.player][1]
                self.history[act.player][street][action.type].append(act)

    def __repr__(self):
        ret = "MATCH HISTORY\n"
        for p in self.history.keys():
            ret += "PLAYER " + p + "\n"
            for s in range(4):
                ret += "    STREET " + str(s) + "\n"
                for a in self.history[p][s].keys():
                    ret += "        ACTION " + ACTION_TYPES[a] + "\n"
                    for i in range(len(self.history[p][s][a])):
                        act = self.history[p][s][a][i]
                        ret += "             ["
                        ret += "TYPE: " + ACTION_TYPES[act.type] + ", "
                        ret += "AMOUNT: " + str(act.amount) + ", "
                        ret += "POT AMOUNT: " + str(act.potAmount) + ", "
                        ret += "BET AMOUNT: " + str(act.betAmount) + ", "
                        ret += "EV: " + str(act.ev[0]) + " " + str(act.ev[1])+ " ]\n"
        return ret[:-1]

    def averageStrength(self, player, game, action, amountType):
        sum = 0
        sum2 = 0
        numMatches = 0
        amountDiffs = [] #list of action values [(action, actionAmount, abs(amount-actionAmount)
        diffBound = max(7,0.15*action.amount)

        #print self.history.keys() ##Need to comment out
        if action.type not in self.history[player.name][action.street].keys():
            print "ACTION TYPE IN AVERAGE STRENGTH", action.type
            return [-1,1000]
        actions = self.history[player.name][action.street][action.type]
        for a in actions:
            ev = a.ev[game.activePlayers-2]
            if amountType==POTAMOUNT:
                if a.potAmount==action.potAmount:
                    sum += ev
                    sum2 += ev*ev
                    numMatches += 1
                else:
                    amountDiffs += [(a, a.potAmount, abs(a.potAmount - action.potAmount))]
            elif amountType==BETAMOUNT:
                if a.betAmount==action.betAmount:
                    sum += ev
                    sum2 += ev*ev
                    numMatches += 1
                else:
                    amountDiffs += [(a, a.betAmount, abs(a.betAmount - action.betAmount))]
            else:
                if a.amount==action.amount:
                    sum += ev
                    numMatches += 1
                    sum2 += ev*ev
                else:
                    diff = abs(a.amount - action.amount)
                    #only use actions within a certain range to calculate average/std values
                    if diff <= diffBound:
                        amountDiffs += [(a, a.amount, diff)]

        if numMatches<3:
           #sort the amountDiffs by the difference in amount from the desired amount
            amountDiffs = sorted(amountDiffs, key=lambda x: x[2])
            minDiff = 0
            for amt in amountDiffs:
                ev = amt[0].ev[game.activePlayers-2]
                if amt[2] != minDiff:
                    minDiff = amt[2]
                    if numMatches>=3:
                        mean = float(sum)/numMatches
                        std = sqrt((sum2*numMatches - (sum*sum))/float(numMatches*(numMatches-1)))
                        return [mean, std]
                sum += ev
                numMatches += 1
                sum2 += ev*ev

            return [-1,1000]

        mean = float(sum)/numMatches
        std = sqrt((sum2*numMatches - (sum*sum))/float(numMatches*(numMatches-1)))
        return [mean, std]
