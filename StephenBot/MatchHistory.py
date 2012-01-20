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

    def updateHistory(self, game, hand):

        pot = game.potSize
        prevBet = game.bigB
        allBets = [0,0,0]
        players = []

        showPlayers = []
        self.showCards = []
        
        for action in hand.actions:
            if action.type == SHOW:
                showPlayers += [action.player]
                self.showCards += [[action.showCard1, action.showCard2]]
        print "SHOWPLAYERS:", showPlayers 
        showEV = [0]*len(showPlayers)


        if len(showPlayers) == 0:
            return

        

        for street in hand.splitActions:  #Preflop, flop, turn, river
            bets = [0,0,0]   #bets for current street for each player
 
            s = hand.splitActions.index(street)
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
                
                if act.player in showPlayers:
                    act.potAmount = act.amount/(pot+sum(bets))
                    act.betAmount = act.amount/float(prevBet)
                    act.handStrength = showEV[showPlayers.index(act.player)]
                    

                if act.player not in self.history.keys():
                    self.history[act.player] = [{},{},{},{}]
                    for a in range(4):#[BET,CALL,CHECK,RAISE]:
                        for s in range(4):
                            self.history[act.player][s][a] = []

                ##Append action into the match history table
                print "HISTORY PRINTOUT", act.player, showPlayers
                if act.player in showPlayers:
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
                        print "BET AMOUNT:", self.history[p][s][a][i].betAmount,
                        print "EV:", self.history[p][s][a][i].handStrength,"]"


