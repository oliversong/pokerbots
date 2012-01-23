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
        if len(game.hand.recentOppMove())==0: #first to act
            if ev>400:
                move = self.pushMin(game,3)
                if move.split(":")[0] != "CHECK":
                    if move.split(":")[1] > 50:
                        move = "CALL"
            elif ev>250:
                move = self.pushMin(game,1)
                if move.split(":")[0] != "CHECK":
                    if move.split(":")[1] > 50:
                        move = "CALL"
            else:
                return self.maxRisk(game,2)
            #move = "CALL"
        elif len(game.hand.recentOppMove())==1: #second to act
            rightOppEv = archive.averageStrength(game.rightOpp,
                                                 0,
                                                 game.hand.actions[-1].type,
                                                 ABSAMOUNT,
                                                 game.lastBet-10,
                                                 game.lastBet+10)
            if rightOppEv == -1:
                if ev>400:
                    move = self.pushMin(game,3)
                    if move.split(":")[0] != "CHECK":
                        if move.split(":")[1] > 50:
                            move = "CALL"
                elif ev>250:
                    move = self.pushMin(game,1)
                    if move.split(":")[0] != "CHECK":
                        if move.split(":")[1] > 50:
                            move = "CALL"
                else:
                    return self.maxRisk(game,2)
#                return self.maxRisk(game,4)
            elif ev > rightOppEv:
                move = self.pushMin(game,3)
                if move.split(":")[0] != "CHECK":
                    if move.split(":")[1] > 50:
                        move = "CALL"
#        move = "CALL"#self.pushMin(game, 1)#"CALL"
            else:
                move = "CHECK"
        else: #any other occurence
            rightAct, leftAct = game.hand.recentOppMove()
            rightOppEv = archive.averageStrength(game.rightOpp, 0,
                                                 rightAct.type,
                                                 ABSAMOUNT,
                                                 rightAct.amount-10,
                                                 rightAct.amount+10)
            leftOppEv = archive.averageStrength(game.leftOpp, 0,
                                                leftAct.type,
                                                ABSAMOUNT,
                                                leftAct.amount-10,
                                                leftAct.amount+10)

            print "RIGHT_EV:", rightOppEv, "LEFT_EV:", leftOppEv, "MY_EV:",ev
            if rightOppEv == -1 or leftOppEv==-1:
                if ev>400:
                    move = self.pushMin(game,3)
                    if move.split(":")[0] != "CHECK":
                        if move.split(":")[1] > 50:
                            move = "CALL"
                elif ev>250:
                    move = self.pushMin(game,1)
                    if move.split(":")[0] != "CHECK":
                        if move.split(":")[1] > 50:
                            move = "CALL"
                else:
                    return self.maxRisk(game,2)
#               return self.maxRisk(game,4)
            elif ev <= rightOppEv or ev <= leftOppEv:
                move = "CHECK"
            else:
                move = self.pushMin(game,3)
                if move.split(":")[0] != "CHECK":
                    if move.split(":")[1] > 50:
                        move = "CALL"
#            move = "CALL"#self.pushMin(game, 5)#"CALL"

        if move not in [la[0] for la in game.legalActions]:
            move = "CHECK"
        return move