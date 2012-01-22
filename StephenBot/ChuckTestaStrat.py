from Strategy import *
from Enums import *

class ChuckTestaStrat(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):

        ev = self.evalHand(game)

        pos = game.position

        move = "CHECK"

#        if game.street()==PREFLOP:
        if len(game.hand.recentOppMove())==0: #dealer
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
        elif len(game.hand.recentOppMove())==1: #small blind
            rightOppEv = archive.averageStrength(game.rightOpp,
                                                              0,
                                                              game.hand.actions[-1].type,
                                                              ABSAMOUNT,
                                                              game.lastBet-10,
                                                              game.lastBet+10)
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
        elif len(game.hand.recentOppMove())==2: #big blind
            rightOppEv = archive.averageStrength(game.rightOpp, 0,
                                                 game.hand.actions[-1].type,
                                                 ABSAMOUNT,
                                                 game.hand.recentOppMove()[0].amount-10,
                                                 game.hand.recentOppMove()[0].amount+10)
            leftOppEv = archive.averageStrength(game.leftOpp, 0,
                                                 game.hand.actions[-2].type,
                                                 ABSAMOUNT,
                                                 game.hand.recentOppMove()[1].amount-10,
                                                 game.hand.recentOppMove()[1].amount+10)

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

        if move not in [la[0] for la in game.legalActions]:
            move = "CHECK"
        return move
