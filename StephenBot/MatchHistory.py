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
        self.showCards = []

    def reset(self, game):
        self.history[game.leftOpp] = [{},{},{},{}]
        self.history[game.rightOpp] = [{},{},{},{}]
        for a in range(4):#[BET,CALL,CHECK,RAISE]:
            for s in range(4):
                self.history[game.leftOpp][s][a] = []
                self.history[game.rightOpp][s][a] = []

    def update(self, game):

        pot = 0
        prevBet = game.bigB
        allBets = [0,0,0]
        players = []

        showPlayers = []
        self.showCards = []

        for action in game.hand.actions:
            if action.type == SHOW:
                showPlayers += [action.player]
                self.showCards += [[action.showCard1, action.showCard2]]
        showEV = [0]*len(showPlayers)


        if len(showPlayers) == 0:
            return



        for street in game.hand.splitActions:  #Preflop, flop, turn, river
            bets = [0,0,0]   #bets for current street for each player

            s = game.hand.splitActions.index(street)
            b = [255,255,255,255,255]
            if s==1: #FLOP
                b = game.boardCards
                b[3] = 255
                b[4] = 255
            elif s==2: #TURN
                b = game.boardCards
                b[4] = 255
            elif s==3: #RIVER
                b = game.boardCards


            for i in range(len(showPlayers)):
                playerHand = self.showCards[i]

                ev = self.pokereval.poker_eval(game="holdem",
                                               pockets =[playerHand,[255,255],[255,255]],
                                               dead = [],
                                               board = b,
                                               iterations = ITERATIONS)
                showEV[i] = ev['eval'][0]['ev']

            for action in street:
                act = action.copy()
                if action.player not in players:
                    players += [action.player]

                act.player = action.player
                act.amount = action.amount

                if act.player in showPlayers and act.type != POST:
                    act.potAmount = act.amount/(pot+sum(bets))
                    act.betAmount = act.amount/float(prevBet)
                    act.handStrength = showEV[showPlayers.index(act.player)]

                if act.player not in self.history.keys():
                    self.history[act.player] = [{},{},{},{}]
                    for a in range(4):#[BET,CALL,CHECK,RAISE]:
                        for s in range(4):
                            self.history[act.player][s][a] = []

                ##Append action into the match history table
                if act.player in showPlayers and act.type != POST:
                    self.history[act.player][game.hand.splitActions.index(street)][action.type].append(act)
                    #print "Action being historied", act.type, "Amt being Historied", act.amount, "Player being historied", act.player, "on street",

                bets[players.index(act.player)] = max([bets[players.index(act.player)],act.amount])
#                print "BETS AMOUNTS:",bets[players.index(act.player)]

                if act.type in [BET, RAISE]:
                    prevBet = act.amount

            prevBet =  0.0000000000000001

            pot += sum(bets)

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


    def averageStrength(self, player, street, actionType, amountType, amount):
        sum = 0
        sum2 = 0
        numMatches = 0
        std = 0

        amountDiffs = [] #list of action values [(action, actionAmount, abs(amount-actionAmount)

        #print self.history.keys() ##Need to comment out
        if actionType not in self.history[player][street].keys():
            print "ACTION TYPE IN AVERAGE STRENGTH", actionType
            return [-1,-1]
        actions = self.history[player][street][actionType]
        for a in actions:
            if amountType==POTAMOUNT:
                if a.potAmount==amount:
                    sum += a.handStrength
                    sum2 += a.handStrength*a.handStrength
                    numMatches += 1
                    mean = float(sum)/numMatches
                    std = sqrt((float(sum2)/numMatches) - (mean*mean))
                else:
                    amountDiffs += [(a, a.potAmount, abs(a.potAmount - amount))]
            elif amountType==BETAMOUNT:
                if a.betAmount==amount:
                    sum += a.handStrength
                    sum2 += a.handStrength*a.handStrength
                    numMatches += 1
                    mean = float(sum)/numMatches
                    std = sqrt((float(sum2)/numMatches) - (mean*mean))
                else:
                    amountDiffs += [(a, a.betAmount, abs(a.betAmount - amount))]
            else:
                if a.amount==amount:
                    sum += a.handStrength
                    numMatches += 1
                    sum2 += a.handStrength*a.handStrength
                    mean = float(sum)/numMatches
                    std = sqrt((float(sum2)/numMatches) - (mean*mean))
                else:
                    amountDiffs += [(a, a.amount, abs(a.amount - amount))]

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

            return [-1,-1]

        return [float(sum)/numMatches, std]
