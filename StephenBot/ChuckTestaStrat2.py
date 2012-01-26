from Strategy import *
from Enums import *
import random

class ChuckTestaStrat2(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):
        ev = self.evalHand(game)
        OppEvs = self.getOppEvs(game, archive)

        move = "CHECK"

        if game.street==PREFLOP:
            if game.activePlayers == 2:
                ev = self.evaluatePocketCards2(game)
            else: 
                ev = self.evaluatePocketCards3(game)

            if ev <275:
                return "CHECK"

            if game.lastBet > 100:
                return "CHECK"

        print "RIGHT EV:", OppEvs[game.rightOpp], "LEFT EV:", OppEvs[game.leftOpp], "EV:", ev, "activePlayers:", game.activePlayers

        if OppEvs[game.rightOpp][0] == -1 and OppEvs[game.leftOpp][0] == -1:
            print "know nothing"
            move = self.blindEVplay(game,ev)
        elif OppEvs[game.rightOpp][0] == -1 or OppEvs[game.leftOpp][0] == -1:
            print "know only one"
            move = self.blindEVplay(game,ev)
            if OppEvs[game.rightOpp][0]-OppEvs[game.rightOpp][1]/2>ev or OppEvs[game.leftOpp][0]-OppEvs[game.leftOpp][1]/2>ev:
                print "and we're worse than the one we know"
                move = "CHECK"
        elif ev > OppEvs[game.rightOpp][0]-OppEvs[game.rightOpp][1]/2 and ev > OppEvs[game.leftOpp][0]-OppEvs[game.leftOpp][1]/2:
            print "know both and we're better"
            move = self.bestEVplay(game)
        else:
            print "know both and we're worse than at least one"
            move = "CHECK"

        if move.split(":")[0] not in [la[0] for la in game.legalActions]:
            print "returned illegal action"
            move = "CHECK"

        return move


    def getOppEvs(self, game, archive):
        OM = self.OppMoves(game)
        OppEvs = {}
        OppEvs[game.rightOpp] = [-1,1000]
        OppEvs[game.leftOpp] = [-1,1000]

        for p in [game.leftOpp, game.rightOpp]:
            if len(OM[p]) == 0:
                OppEvs[p] = [-1,1000]
                continue

            lastAction = OM[p][-1][1]
            if lastAction.type == FOLD:
                OppEvs[p] = [0,1000]
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

    def OppMoves(self, game):
        OM = {}
        OM[game.rightOpp]=[]
        OM[game.leftOpp] =[]
        game.hand.splitActionsList()
        for s,street in enumerate(game.hand.splitActions):
            for acts in street:
                if acts.type != POST:
                    if acts.player in OM.keys():
                        OM[acts.player] += [(s,acts)]
        return OM

    def blindEVplay(self, game, ev):
        street = game.street
        if street == PREFLOP:
            npm = 0
            if game.activePlayers == 2:
                npm = 160
            move = "CHECK"
            if ev>600+npm:
                move = self.pushMin(game,random.randint(4,10))
                if move.split(":")[0] in ["BET", "RAISE"]:
                    if int(move.split(":")[1]) > 200:
                        move = "CALL"
            elif ev>400+npm:
                move = self.pushMin(game,random.randint(1,4))
                if move.split(":")[0] in ["BET", "RAISE"]:
                    if int(move.split(":")[1]) > 30:
                        move = "CALL"
            elif ev>300+npm:
                move = self.maxRisk(game,10)
            else:
                move =  self.maxRisk(game,2)
        elif street == FLOP:
            move = "CHECK"
            if ev>700:
                move = self.pushMin(game,random.randint(4,10))
                if move.split(":")[0] in ["BET", "RAISE"]:
                    if int(move.split(":")[1]) > 200:
                        move = "CALL"
            elif ev>500:
                move = self.pushMin(game,random.randint(1,4))
                if move.split(":")[0] in ["BET", "RAISE"]:
                    if int(move.split(":")[1]) > 50:
                        move = "CALL"
            else:
                move =  self.maxRisk(game,2)
        elif street == TURN:
            move = "CHECK"
            if ev>800:
                move = self.pushMin(game,10)
                if move.split(":")[0] in ["BET", "RAISE"]:
                    if int(move.split(":")[1]) > 200:
                        move = "CALL"
            elif ev>600:
                move = self.pushMin(game,random.randint(1,4))
                if move.split(":")[0] in ["BET", "RAISE"]:
                    if int(move.split(":")[1]) > 50:
                        move = "CALL"
            elif ev>500:
                move = self.maxRisk(game,10)
            else:
                move =  self.maxRisk(game,2)
        elif street == RIVER:
            move = "CHECK"
            if ev>800:
                move = self.pushMin(game,random.randint(4,10))
                if move.split(":")[0] in ["BET", "RAISE"]:
                    if int(move.split(":")[1]) > 200:
                        move = "CALL"
            elif ev>650:
                move = self.pushMin(game,random.randint(1,4))
                if move.split(":")[0] in ["BET", "RAISE"]:
                    if int(move.split(":")[1]) > 50:
                        move = "CALL"
            elif ev>500:
                move = self.maxRisk(game,10)
            else:
                move =  self.maxRisk(game,2)
        else:
            print "Error! You reached a state not 0-3! in blindEVplay"

        return move


    def bestEVplay(self, game):
        street = game.street
        if street == PREFLOP:
            move = self.pushMin(game,random.randint(2,6))
            if move.split(":")[0] in ["BET", "RAISE"]:
                if int(move.split(":")[1]) > 30:
                    move = "CALL"
        elif street == FLOP:
            move = self.pushMin(game,random.randint(3,7))
            if move.split(":")[0] in ["BET", "RAISE"]:
                if int(move.split(":")[1]) > 40:
                    move = "CALL"
        elif street == TURN:
            move = self.pushMin(game,random.randint(4,8))
            if move.split(":")[0] in ["BET", "RAISE"]:
                if int(move.split(":")[1]) > 50:
                    move = "CALL"
        elif street == RIVER:
            move = self.pushMin(game,10)
        else:
            print "Error! You reached a state not 0-3! in bestEVplay"

        return move
