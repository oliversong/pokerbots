from Strategy import *
from Enums import *

class ChuckTestaStrat(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def evaluateOdds(self, b):
        self.evaluatePocketCards(b)
        self.evalHand(b, b.game.boardCards)

    def getMove(self, b):

        ev = self.evalHand(b, b.game.boardCards)

        pos = b.game.position

        move = "CHECK"

#        if b.game.street()==PREFLOP:
        if len(b.game.hand.recentOppMove())==0: #dealer
            if ev>400:
                move = self.pushMin(b,3)
                if move.split(":")[0] != "CHECK":
                    if move.split(":")[1] > 50:
                        move = "CALL"
            elif ev>250:
                move = self.pushMin(b,1)
                if move.split(":")[0] != "CHECK":
                    if move.split(":")[1] > 50:
                        move = "CALL"
            else:
                return self.maxRisk(b,2)
            #move = "CALL"
        elif len(b.game.hand.recentOppMove())==1: #small blind
            rightOppEv = b.game.matchHistory.averageStrength(b.game.rightOpp,
                                                              0,
                                                              b.game.hand.actions[-1].type,
                                                              ABSAMOUNT,
                                                              b.game.lastBet-10,
                                                              b.game.lastBet+10)
            if rightOppEv == -1:
                if ev>400:
                    move = self.pushMin(b,3)
                    if move.split(":")[0] != "CHECK":
                        if move.split(":")[1] > 50:
                            move = "CALL"
                elif ev>250:
                    move = self.pushMin(b,1)
                    if move.split(":")[0] != "CHECK":
                        if move.split(":")[1] > 50:
                            move = "CALL"
                else:
                    return self.maxRisk(b,2)
#                return self.maxRisk(b,4)
            elif ev > rightOppEv:
                move = self.pushMin(b,3)
                if move.split(":")[0] != "CHECK":
                    if move.split(":")[1] > 50:
                        move = "CALL"
#        move = "CALL"#self.pushMin(b, 1)#"CALL"
            else:
                move = "CHECK"
        elif len(b.game.hand.recentOppMove())==2: #big blind
            rightOppEv = b.game.matchHistory.averageStrength(b.game.rightOpp, 0,
                                                 b.game.hand.actions[-1].type,
                                                 ABSAMOUNT,
                                                 b.game.hand.recentOppMove()[0].amount-10,
                                                 b.game.hand.recentOppMove()[0].amount+10)
            leftOppEv = b.game.matchHistory.averageStrength(b.game.leftOpp, 0,
                                                 b.game.hand.actions[-2].type,
                                                 ABSAMOUNT,
                                                 b.game.hand.recentOppMove()[1].amount-10,
                                                 b.game.hand.recentOppMove()[1].amount+10)

            print "RIGHT_EV:", rightOppEv, "LEFT_EV:", leftOppEv, "MY_EV:",ev
            if rightOppEv == -1 or leftOppEv==-1:
                if ev>400:
                    move = self.pushMin(b,3)
                    if move.split(":")[0] != "CHECK":
                        if move.split(":")[1] > 50:
                            move = "CALL"
                elif ev>250:
                    move = self.pushMin(b,1)
                    if move.split(":")[0] != "CHECK":
                        if move.split(":")[1] > 50:
                            move = "CALL"
                else:
                    return self.maxRisk(b,2)
#               return self.maxRisk(b,4)
            elif ev <= rightOppEv or ev <= leftOppEv:
                move = "CHECK"
            else:
                move = self.pushMin(b,3)
                if move.split(":")[0] != "CHECK":
                    if move.split(":")[1] > 50:
                        move = "CALL"
#            move = "CALL"#self.pushMin(b, 5)#"CALL"

        if move not in [la[0] for la in b.game.legalActions]:
            move = "CHECK"
        return move
