from Strategy import *
from Enums import *
from Move import *
import random

class ChuckTestaStrat(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):
        # Calculate our ev
        ev = self.evalHand(game)

        #if game.street==PREFLOP:
        #    if ev <275:
        #        return "CHECK"

        OppEvs = self.getOppEvs(game, archive)

        move = Move(CHECK)

        print "RIGHT EV:", OppEvs[game.rightOpp.name], "LEFT EV:", OppEvs[game.leftOpp.name], "EV:", ev, "activePlayers:", game.activePlayers

        p1ev = OppEvs[game.rightOpp.name][0]
        p1stdev = OppEvs[game.rightOpp.name][1]
        p2ev = OppEvs[game.leftOpp.name][0]
        p2stdev = OppEvs[game.leftOpp.name][1]
        comment = ""
        
        if p1ev == -1 and p2ev == -1:
            move = self.blindEVplay(game,ev)
            if game.activePlayers == 3:
                comment = "3 players: know nothing"
            elif game.activePlayers ==2:
                comment = "2 players: know nothing"
            else:
                comment = "Know Nothing and neither 3 or 2 players in game, there are", game.activePlayers, "players"
        elif game.activePlayers == 3:
            if p1ev == -1 or p2ev == -1:
                comment = "3 players: know only one EV"
                move = self.blindEVplay(game,ev)
                if p1ev-p1stdev>ev or p2ev-p2stdev>ev:
                    comment += " and we're worse by a STD"
                    move = Move(CHECK)
                elif p1ev>ev or p2ev>ev:
                    comment += " and we're worse by less than a STD"
                    move = self.maxRisk(game,4)
            else:
                comment = "3 players: know both EV"
                if ev>p1ev+p1stdev and ev>p2ev+p2stdev:
                    comment += " and we're better than both by a STD"
                    move = self.bestEVplay(game)
                elif ev>p1ev and ev>p2ev:
                    comment += " and we're better than both by less than a STD"
                    move = self.goodEVplay(game)
                elif ev>p1ev-p1stdev and ev>p2ev-p2stdev:
                    comment += " and we're worse than both by less than a STD"
                    move = self.maxRisk(game,10)
                else:
                    comment += " and we're worse than atleast one by a STD"
                    move = Move(CHECK)
        elif game.activePlayers == 2:
            ##We must know our opp EV since both opp EV!=-1
            ##If on preflop we need to scale our EV
            if game.street == PREFLOP:
                ev = ev-160

            ##need to eliminate STD of player not in to not interfere with logic below
            if p1ev == -1:
                p1stdev = 0
            elif p2ev == -1:
                p2stdev = 0

            comment = "2 players: know his EV "
            if ev>p1ev+p1stdev and ev>p2ev+p2stdev:
                comment += " and we're better than his by a STD"
                move = self.bestEVplay(game)
            elif ev>p1ev and ev>p2ev:
                comment += " and we're better than his by less than a STD"
                move = self.goodEVplay(game)
            elif ev>p1ev-p1stdev and ev>p2ev-p2stdev:
                comment += " and we're worse than his by less than a STD"
                move = self.maxRisk(game,10)
            else:
                comment += " and we're worse than his by a STD"
                move = Move(CHECK)
        else:
            comment = "Neither 3 or 2 player game, there are", game.activePlayers, "players"


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

            absamt = archive.averageStrength(p, game, lastAction, ABSAMOUNT)

            if lastAction.type == CHECK:
                OppEvs[p] = absamt
                continue

            potamt = archive.averageStrength(p, game, lastAction, POTAMOUNT)

            if lastAction.type in [BET, CALL]:
                OppEvs[p] = min(absamt,potamt,key=lambda x:x[1])
            elif lastAction.type == RAISE:
                betamt = archive.averageStrength(p, game, lastAction, BETAMOUNT)
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

    def goodEVplay(self, game):
        street = game.street
        if street == PREFLOP:
            move = self.pushMin(game,random.randint(2,6))
            if move.type in [BET, RAISE]:
                if move.amount > 10:
                    move = Move(CALL)
        elif street == FLOP:
            move = self.pushMin(game,random.randint(3,7))
            if move.type in [BET, RAISE]:
                if move.amount > 20:
                    move = Move(CALL)
        elif street == TURN:
            move = self.pushMin(game,random.randint(4,8))
            if move.type in [BET, RAISE]:
                if move.amount > 20:
                    move = Move(CALL)
        elif street == RIVER:
            move = self.pushMin(game,random.randint(4,8))
            if move.type in [BET, RAISE]:
                if move.amount > 20:
                    move = Move(CALL)
        else:
            print "Error! You reached a state not 0-3! in bestEVplay"

        return move
