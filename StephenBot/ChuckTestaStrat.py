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

        #p1ev = OppEvs[game.rightOpp.name][0]
        #p1stdev = OppEvs[game.rightOpp.name][1]
        #p2ev = OppEvs[game.leftOpp.name][0]
        #p2stdev = OppEvs[game.leftOpp.name][1]

        scores = {}#{game.rightOpp.name:UNKNOWN,game.leftOpp.name:UNKNOWN}
        for pname,p in OppEvs.items():
            if p[0] == -1:
                scores[pname] = UNKNOWN
            elif ev>p[0]+p[1]:
                scores[pname] = BEST
            elif ev>p[0]:
                scores[pname] = GOOD
            elif ev>p[0]-p[1]:
                scores[pname] = OK
            else:
                scores[pname] = BAD

        print "RIGHT EV:", OppEvs[game.rightOpp.name],"-",scores[game.rightOpp.name], "LEFT EV:", OppEvs[game.leftOpp.name],"-",scores[game.leftOpp.name], "EV:", ev, "activePlayers:", game.activePlayers
        comment = ""

        if scores[game.rightOpp.name] == UNKNOWN and scores[game.leftOpp.name] == UNKNOWN:
            move = self.blindEVplay(game,ev)
            if game.activePlayers == 3:
                comment = "3 players: know nothing"
            elif game.activePlayers ==2:
                comment = "2 players: know nothing"
            else:
                comment = "Know Nothing and neither 3 or 2 players in game, there are", game.activePlayers, "players"
        elif game.activePlayers == 3:
            if UNKNOWN in scores.values():
                score = scores[game.leftOpp.name]
                if score == UNKNOWN:
                    score = scores[game.rightOpp.name]
                comment = "3 players: know only one EV"

                if score == BAD:
                    comment += " and we're worse by a STD"
                    move = Move(CHECK)
                elif score == OK:
                    comment += " and we're worse by less than a STD"
                    move = self.maxRisk(game,4)
                else:
                    comment += " and we're better"
                    move = self.blindEVplay(game,ev)
            else:
                comment = "3 players: know both EV"
                if BAD in scores.values():
                    comment += " and we're worse than at least one by a STD"
                    move = Move(CHECK)
                elif OK in scores.values():
                    comment += " and we're worse than at least one by less than a STD"
                    move = self.maxRisk(game,10)
                elif GOOD in scores.values():
                    comment += " and we're better than both, but within a STD of at least one"
                    move = self.goodEVplay(game)
                else:
                    comment += " and we're better than both by a STD"
                    move = self.bestEVplay(game)
        elif game.activePlayers == 2:
            ##We must know our opp EV since both opp EV!=-1
            score = scores[game.leftOpp.name]
            if not game.leftOpp.active:
                score = scores[game.rightOpp.name]

            comment = "2 players: know his EV"
            if score == BAD:
                comment += " and we're worse than his by a STD"
                move = Move(CHECK)
            elif score == OK:
                comment += " and we're worse than his by less than a STD"
                move = self.maxRisk(game,10)
            elif score == GOOD:
                comment += " and we're better than his by less than a STD"
                move = self.goodEVplay(game)
            else:
                comment += " and we're better than his by a STD"
                move = self.bestEVplay(game)
        else:
            comment = "Neither 3 or 2 player game, there are", game.activePlayers, "players"


        #print comment
        if ACTION_TYPES[move.type] not in [la[0] for la in game.legalActions]:
            print "returned illegal action",move,"! in",game.legalActions
            move = Move(CHECK)

        move.rightEV = OppEvs[game.rightOpp.name]
        move.leftEV = OppEvs[game.leftOpp.name]
        move.myEV = ev
        move.comment = comment

        return move

    def getOppEvs(self, game, archive):
        OppEvs = {}
        OppEvs[game.rightOpp.name] = [-1,1000]
        OppEvs[game.leftOpp.name] = [-1,1000]

        for p in [game.leftOpp, game.rightOpp]:
            if len(p.lastActions) == 0:
                OppEvs[p.name] = [-1,1000]
                continue

            lastAction = p.lastActions[-1]
            if lastAction.type == FOLD:
                OppEvs[p.name] = [-1,1000]
                continue

            absamt = archive.averageStrength(p, game, lastAction, ABSAMOUNT)

            if lastAction.type == CHECK:
                OppEvs[p.name] = absamt
                continue

            potamt = archive.averageStrength(p, game, lastAction, POTAMOUNT)

            if lastAction.type in [BET, CALL]:
                OppEvs[p.name] = min(absamt,potamt,key=lambda x:x[1])
            elif lastAction.type == RAISE:
                betamt = archive.averageStrength(p, game, lastAction, BETAMOUNT)
                OppEvs[p.name] = min(absamt,betamt,potamt,key=lambda x:x[1])
        return OppEvs

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
