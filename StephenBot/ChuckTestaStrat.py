from Strategy import *
from Enums import *
from Move import *
import random

class ChuckTestaStrat(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):
        # Calculate our ev
        if game.street==PREFLOP:
            if game.activePlayers == 2:
                ev = self.evaluatePocketCards2(game)
            else:
                ev = self.evaluatePocketCards3(game)

            #if ev <275:
            #    return "CHECK"

        else:
            ev = self.evalHand(game)

        OppEvs = self.getOppEvs(game, archive)

        move = Move(CHECK)

        print "RIGHT EV:", OppEvs[game.rightOpp.name], "LEFT EV:", OppEvs[game.leftOpp.name], "EV:", ev, "activePlayers:", game.activePlayers

        comment = ""
        if OppEvs[game.rightOpp.name][0] == -1 and OppEvs[game.leftOpp.name][0] == -1:
            comment = "know nothing"
            move = self.blindEVplay(game,ev)
        elif game.activePlayers == 2:
            comment = "Only playing one player"
            if ev > OppEvs[game.rightOpp.name][0]+OppEvs[game.rightOpp.name][1]/2 and ev > OppEvs[game.leftOpp.name][0]+OppEvs[game.leftOpp.name][1]/2:
                comment += " and we know we're better"
                move = self.bestEVplay(game)
            else:
                comment += " and we know we're worse"
                move = Move(CHECK)
        elif OppEvs[game.rightOpp.name][0] == -1 or OppEvs[game.leftOpp.name][0] == -1:
            comment = "know only one EV"
            move = self.blindEVplay(game,ev)
            if OppEvs[game.rightOpp.name][0]>ev or OppEvs[game.leftOpp.name][0]>ev:
                comment += " and we're worse"
                move = Move(CHECK)
        elif ev > OppEvs[game.rightOpp.name][0]+OppEvs[game.rightOpp.name][1]/2 and ev > OppEvs[game.leftOpp.name][0]+OppEvs[game.leftOpp.name][1]/2:
            comment = "know both and we're better than both"
            move = self.bestEVplay(game)
        else:
            comment = "know both and we're worse than at least one"
            move = Move(CHECK)
        #print comment
        if ACTION_TYPES[move.type] not in [la[0] for la in game.legalActions]:
            print "returned illegal action"
            move = Move(CHECK)

        move.rightEV = OppEvs[game.rightOpp.name]
        move.leftEV = OppEvs[game.leftOpp.name]
        move.myEV = ev
        move.comment = comment

        return move


    def getOppEvs(self, game, archive):
        OM = self.OppMoves(game)
        OppEvs = {}
        OppEvs[game.rightOpp.name] = [-1,1000]
        OppEvs[game.leftOpp.name] = [-1,1000]

        for p in [game.leftOpp.name, game.rightOpp.name]:
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
        OM[game.rightOpp.name]=[]
        OM[game.leftOpp.name] =[]
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
            move = Move(CHECK)
            if ev>600+npm:
                move = self.pushMin(game,random.randint(4,10))
                if move.type in [BET, RAISE]:
                    if move.amount > 200:
                        move = Move(CALL)
            elif ev>400+npm:
                move = self.pushMin(game,random.randint(1,4))
                if move.type in [BET, RAISE]:
                    if move.amount > 30:
                        move = Move(CALL)
            elif ev>300+npm:
                move = self.maxRisk(game,10)
            else:
                move =  self.maxRisk(game,2)
        elif street == FLOP:
            move = Move(CHECK)
            if ev>700:
                move = self.pushMin(game,random.randint(4,10))
                if move.type in [BET, RAISE]:
                    if move.amount > 200:
                        move = Move(CALL)
            elif ev>500:
                move = self.pushMin(game,random.randint(1,4))
                if move.type in [BET, RAISE]:
                    if move.amount > 50:
                        move = Move(CALL)
            else:
                move =  self.maxRisk(game,2)
        elif street == TURN:
            move = Move(CHECK)
            if ev>800:
                move = self.pushMin(game,10)
                if move.type in [BET, RAISE]:
                    if move.amount > 200:
                        move = Move(CALL)
            elif ev>600:
                move = self.pushMin(game,random.randint(1,4))
                if move.type in [BET, RAISE]:
                    if move.amount > 50:
                        move = Move(CALL)
            elif ev>500:
                move = self.maxRisk(game,10)
            else:
                move =  self.maxRisk(game,2)
        elif street == RIVER:
            move = Move(CHECK)
            if ev>800:
                move = self.pushMin(game,random.randint(4,10))
                if move.type in [BET, RAISE]:
                    if move.amount > 200:
                        move = Move(CALL)
            elif ev>650:
                move = self.pushMin(game,random.randint(1,4))
                if move.type in [BET, RAISE]:
                    if move.amount > 50:
                        move = Move(CALL)
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
            if move.type in [BET, RAISE]:
                if move.amount > 30:
                    move = Move(CALL)
        elif street == FLOP:
            move = self.pushMin(game,random.randint(3,7))
            if move.type in [BET, RAISE]:
                if move.amount > 40:
                    move = Move(CALL)
        elif street == TURN:
            move = self.pushMin(game,random.randint(4,8))
            if move.type in [BET, RAISE]:
                if move.amount > 50:
                    move = Move(CALL)
        elif street == RIVER:
            move = self.pushMin(game,10)
        else:
            print "Error! You reached a state not 0-3! in bestEVplay"

        return move
