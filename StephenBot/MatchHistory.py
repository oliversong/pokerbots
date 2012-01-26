from math import *
from Action import *
from Hand import *
from GameState import *
from Enums import *

from pokereval import PokerEval

ITERATIONS = 100000

class MatchHistory:
    def __init__(self):
        self.history = {}
        self.pokereval = PokerEval()

    def reset(self, game):
        self.history[game.leftOpp] = [{},{},{},{}]
        self.history[game.rightOpp] = [{},{},{},{}]
        for a in range(4):#[BET,CALL,CHECK,RAISE]:
            for s in range(4):
                self.history[game.leftOpp][s][a] = []
                self.history[game.rightOpp][s][a] = []

    def update(self, game):
        showPlayers = []
        showCards = []

        for action in game.hand.actions:
            if action.type == SHOW and action.player in self.history.keys():
                showPlayers += [action.player]
                showCards += [[action.showCard1, action.showCard2]]

        if len(showPlayers) == 0:
            return
        showEV = [0]*len(showPlayers)

        for s,street in enumerate(game.hand.splitActions):  #Preflop, flop, turn, river
            b = [255]*5
            if s==FLOP: #FLOP
                b[:3] = game.boardCards[:3]
            elif s==TURN: #TURN
                b[:4] = game.boardCards[:4]
            elif s==RIVER: #RIVER
                b = game.boardCards

            for i in range(len(showPlayers)):
                playerHand = showCards[i]
                ev = self.pokereval.poker_eval(game="holdem",
                                               pockets =[playerHand,[255,255],[255,255]],
                                               dead = [],
                                               board = b,
                                               iterations = ITERATIONS)
                showEV[i] = ev['eval'][0]['ev']

            for action in street:
                if action.player in showPlayers and action.type != POST:
                    act = action.copy()
                    act.handStrength = showEV[showPlayers.index(action.player)]
                    self.history[act.player][s][action.type].append(act)
                    #print "Appending action: " + str(act)

            #self.printHistory()

    def printHistory(self):
        print "PRINTING HISTORY"
#        print self.history.keys()
        for p in self.history.keys():
            print "PLAYER",p
            for s in range(4):
                print "    STREET", s
                for a in self.history[p][s].keys():
                    print "        ACTION", a
                    for i in range(len(self.history[p][s][a])):
                        print "             [",
                        print "TYPE:", self.history[p][s][a][i].type,",",
                        print "PLAYER:", self.history[p][s][a][i].player,",",
                        print "AMOUNT:", self.history[p][s][a][i].amount,",",
                        print "POT AMOUNT:",self.history[p][s][a][i].potAmount,",",
                        print "BET AMOUNT:", self.history[p][s][a][i].betAmount,
                        print "EV:", self.history[p][s][a][i].handStrength,"]"

    def averageStrength(self, player, street, action, amountType):
        sum = 0
        sum2 = 0
        numMatches = 0
        std = 0

        amountDiffs = [] #list of action values [(action, actionAmount, abs(amount-actionAmount)

        #print self.history.keys() ##Need to comment out
        if action.type not in self.history[player][street].keys():
            print "ACTION TYPE IN AVERAGE STRENGTH", action.type
            return [-1,200]
        actions = self.history[player][street][action.type]
        for a in actions:
            if amountType==POTAMOUNT:
                if a.potAmount==action.potAmount:
                    sum += a.handStrength
                    sum2 += a.handStrength*a.handStrength
                    numMatches += 1
                    mean = float(sum)/numMatches
                    std = sqrt((float(sum2)/numMatches) - (mean*mean))
                else:
                    amountDiffs += [(a, a.potAmount, abs(a.potAmount - action.potAmount))]
            elif amountType==BETAMOUNT:
                if a.betAmount==action.betAmount:
                    sum += a.handStrength
                    sum2 += a.handStrength*a.handStrength
                    numMatches += 1
                    mean = float(sum)/numMatches
                    std = sqrt((float(sum2)/numMatches) - (mean*mean))
                else:
                    amountDiffs += [(a, a.betAmount, abs(a.betAmount - action.betAmount))]
            else:
                if a.amount==action.amount:
                    sum += a.handStrength
                    numMatches += 1
                    sum2 += a.handStrength*a.handStrength
                    mean = float(sum)/numMatches
                    std = sqrt((float(sum2)/numMatches) - (mean*mean))
                else:
                    amountDiffs += [(a, a.amount, abs(a.amount - action.amount))]

        if numMatches<3:
           #sort the amountDiffs by the difference in amount from the desired amount
            amountDiffs = sorted(amountDiffs, key=lambda x: x[2])
            minDiff = 0
            for amt in amountDiffs:
                if amt[2] != minDiff:
                    minDiff = amt[2]
                    if numMatches>=3:
                        return [float(sum)/numMatches, std]
                sum += amt[0].handStrength
                numMatches += 1
                sum2 += amt[0].handStrength*amt[0].handStrength
                mean = float(sum)/numMatches
                std = sqrt((float(sum2)/numMatches) - (mean*mean))

            return [-1,200]

        return [float(sum)/numMatches, std]
