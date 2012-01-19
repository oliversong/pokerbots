from Action import *
from Hand import *
from GameState import *

class MatchHistory:
    def __init__(self):
        self.history = {}

    def updateHistory(self, game, hand):

        pot = 3
        prevBet = game.bigB
        allBets = [0,0,0]
        players = []

        for street in hand.splitActions:  #Preflop, flop, turn, river
            bets = [0,0,0]   #bets for current street for each player

            for action in street:
                act = action.copy()
                if action.player not in players:
                    players += [action.player]

                act.player = action.player
                act.amount = action.amount

                act.potAmount = act.amount/(pot+sum(bets))
                act.betAmount = act.amount/float(prevBet)
                act.amount = act.amount
                act.handStrength = action.handStrength

                if act.player not in self.history.keys():
                    self.history[act.player] = [{},{},{},{}]
                    for a in range(4):#[BET,CALL,CHECK,RAISE]:
                        for s in range(4):
                            self.history[act.player][s][a] = []
                    
        #        if act.handStrength >=0:
                self.history[act.player][hand.splitActions.index(street)][action.type].append(act)

                bets[players.index(act.player)] = max([bets[players.index(act.player)],act.amount])

                if act.amount != 0:
                    prevBet = act.amount
            
            prevBet =  0.0000000000000001

            pot += sum(bets)

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
                        print "BET AMOUNT:", self.history[p][s][a][i].betAmount,"]"


