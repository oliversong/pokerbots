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

        for p in [game.leftOpp, game.rightOpp]:
            if len(OM[p]) == 0:
                OppEvs[p] = [-1,-1]
                continue

            lastAction = OM[p][-1][1]
            if lastAction.type == FOLD:
                OppEvs[p] = [0,-1]
                continue

            absamt = archive.averageStrength(p, game.street,
                                             lastAction, ABSAMOUNT)

            if lastAction.type == CHECK:
                OppEvs[p] = absamt
                continue

            potamt = archive.averageStrength(p, game.street,
                                             lastAction, POTAMOUNT)

            if lastAction.type in [BET, CALL]:
                OppEvs[p] = min(absamt,potamt,key=lambda x:x[1])
            elif lastAction.type == RAISE:
                betamt = archive.averageStrength(p, game.street,
                                                 lastAction, BETAMOUNT)
                OppEvs[p] = min(absamt,betamt,potamt,key=lambda x:x[1])
        return OppEvs

    #Return list of last moves made by each opponent
    def OppMoves(self, game):
        OM = {}
        OM[game.rightOpp]=[]
        OM[game.leftOpp] =[]
        st = 0 #Are there 3 DEAL actions at the beginning of the game?
                #I want st = 0 during the PREFLOP
        game.hand.splitActionsList()
        for s,street in enumerate(game.hand.splitActions):
            for acts in street:
                if acts.type != POST:
                    if acts.player in OM.keys():
                        OM[acts.player] += [(s,acts)]
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
