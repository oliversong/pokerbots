from Strategy import *
from Enums import *

class ChuckTestaStrat2(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):

        ev = self.evalHand(game)
        OppEvs = self.getOppEvs(game, archive)

        pos = game.position
        move = "CHECK"

#        if game.street()==PREFLOP:

##        print "RIGHT EV:", OppEvs[game.rightOpp], "LEFT EV:", OppEvs[game.leftOpp], "EV:", ev

        if OppEvs[game.rightOpp][0] == -1 and OppEvs[game.leftOpp][0] == -1:
            move = self.blindEVplay(game,ev)
        elif ev > OppEvs[game.rightOpp][0]-OppEvs[game.rightOpp][1]/2 and ev > OppEvs[game.leftOpp][0]-OppEvs[game.leftOpp][1]/2:
            move = self.bestEVplay(game,ev)
        elif OppEvs[game.rightOpp][0] == -1 or OppEvs[game.leftOpp][0] == -1:
            move = self.blindEVplay(game,ev)
            if OppEvs[game.rightOpp][0]-OppEvs[game.rightOpp][1]/2>ev or OppEvs[game.leftOpp][0]-OppEvs[game.leftOpp][1]/2>ev:
                move = "CHECK"
        else:
            move = "CHECK"

        if move.split(":")[0] not in [la[0] for la in game.legalActions]:
            move = "CHECK"

        return move


    def getOppEvs(self, game, archive):
        OM = self.OppMoves(game)
        OppEvs = {}
        OppEvs[game.rightOpp] = [-1,-1]
        OppEvs[game.leftOpp] = [-1,-1]


        if len(OM[game.rightOpp]) == 0:
            OppEvs[game.rightOpp] = [-1,-1]
#            print ("No Previous Move on right")
        elif OM[game.rightOpp][-1][1].type == FOLD:
            OppEvs[game.rightOpp] = [0,-1]
        elif OM[game.rightOpp][-1][1].type == CHECK:
            OppEvs[game.rightOpp] = archive.averageStrength(game.rightOpp,
                                                            OM[game.rightOpp][-1][0],
                                                            OM[game.rightOpp][-1][1].type,
                                                            ABSAMOUNT,
                                                            OM[game.rightOpp][-1][1].amount)
        elif OM[game.rightOpp][-1][1].type in [BET, RAISE]:
            absamt = archive.averageStrength(game.rightOpp,
                                             OM[game.rightOpp][-1][0],
                                             OM[game.rightOpp][-1][1].type,
                                             ABSAMOUNT,
                                             OM[game.rightOpp][-1][1].amount)
            betamt = archive.averageStrength(game.rightOpp,
                                             OM[game.rightOpp][-1][0],
                                             OM[game.rightOpp][-1][1].type,
                                             BETAMOUNT,
                                             OM[game.rightOpp][-1][2])
            if absamt[1]<betamt[1]:
                OppEvs[game.rightOpp] = absamt
#                print"Abs Amount EV for Right"
            else:
                OppEvs[game.rightOpp] = betamt
#                print"Bet Amt EV for Right", betamt[0]
#                print  OM[game.rightOpp][-1][2]
        elif OM[game.rightOpp][-1][1].type == CALL:
            OppEvs[game.rightOpp] = archive.averageStrength(game.rightOpp,
                                                            OM[game.rightOpp][-1][0],
                                                            OM[game.rightOpp][-1][1].type,
                                                            ABSAMOUNT,
                                                            OM[game.rightOpp][-1][1].amount)
#        else:
#            print "getOppEvs is broken", OM[game.leftOpp][-1][1].type


        if len(OM[game.leftOpp]) ==0:
            OppEvs[game.leftOpp] = [-1,-1]
#            print "No previous move on left"
        elif OM[game.leftOpp][-1][1].type == FOLD:
            OppEvs[game.leftOpp] = [0,-1]
        elif OM[game.leftOpp][-1][1].type == CHECK:
            OppEvs[game.leftOpp] = archive.averageStrength(game.leftOpp,
                                                           OM[game.leftOpp][-1][0],
                                                           OM[game.leftOpp][-1][1].type,
                                                           ABSAMOUNT,
                                                           OM[game.leftOpp][-1][1].amount)
        elif OM[game.leftOpp][-1][1].type in [BET, RAISE]:
            absamt = archive.averageStrength(game.leftOpp,
                                             OM[game.leftOpp][-1][0],
                                             OM[game.leftOpp][-1][1].type,
                                             ABSAMOUNT,
                                             OM[game.leftOpp][-1][1].amount)
            betamt = archive.averageStrength(game.leftOpp,
                                             OM[game.leftOpp][-1][0],
                                             OM[game.leftOpp][-1][1].type,
                                             BETAMOUNT,
                                             OM[game.leftOpp][-1][2])
            if absamt[1]<betamt[1]:
                OppEvs[game.leftOpp] = absamt
            else:
                OppEvs[game.leftOpp] = betamt
        elif OM[game.leftOpp][-1][1].type == CALL:
            OppEvs[game.leftOpp] = archive.averageStrength(game.leftOpp,
                                                           OM[game.leftOpp][-1][0],
                                                           OM[game.leftOpp][-1][1].type,
                                                           ABSAMOUNT,
                                                           OM[game.leftOpp][-1][1].amount)
#        else:
#            print "getOppEvs is broken", OM[game.leftOpp][-1][1].type



        return OppEvs

    #Return list of last moves made by each opponent
    def OppMoves(self, game):
        OM = {}
        OM[game.rightOpp]=[]
        OM[game.leftOpp] =[]
        st = 0 #Are there 3 DEAL actions at the beginning of the game?
                #I want st = 0 during the PREFLOP
        prevbet = 2

        for acts in game.hand.actions:
            if acts.type == DEAL:
                st+=1
                prevbet = 0
            elif acts.type != POST:
                if acts.type in [CALL, CHECK, FOLD, BET]:
                    betperc = 0
                    if acts.type == BET:
                        prevbet = acts.amount
                elif acts.type == RAISE:
                    betperc = acts.amount/prevbet
#                else:
#                    print "ERRROR IN OPPMOVES"
                if acts.player == game.rightOpp:
                    OM[game.rightOpp] += [(st,acts,betperc)]
                if acts.player == game.leftOpp:
                    OM[game.leftOpp] += [(st,acts,betperc)]

        return OM

    # Play when we don't know our opponents EV
    def blindEVplay(self, game, ev):
        move = "CHECK"
        if ev>400:
            move = self.pushMin(game,10)
            if move.split(":")[0] in [BET, RAISE]:
                if int(move.split(":")[1]) > 50:
                    move = "CALL"
        elif ev>300:
            move = self.pushMin(game,4)
            if move.split(":")[0] in [BET, RAISE]:
                if int(move.split(":")[1]) > 50:
                    move = "CALL"
        else:
            move =  self.maxRisk(game,2)

#        print "BLIND EV PLAY:", move
        return move


    def bestEVplay(self, game, ev):
        move = self.pushMin(game,5)
        if move.split(":")[0] in [BET, RAISE]:
            if int(move.split(":")[1]) > 50:
                move = "CALL"
#        print "BEST EV PLAY:", move
        return move
