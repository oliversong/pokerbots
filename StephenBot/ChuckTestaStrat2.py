from Strategy import *
from Enums import *
from Move import *
import random

class ChuckTestaStrat2(Strategy):
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

        print "RIGHT EV:", OppEvs[game.rightOpp], "LEFT EV:", OppEvs[game.leftOpp], "EV:", ev, "activePlayers:", game.activePlayers

        if OppEvs[game.rightOpp][0] == -1 and OppEvs[game.leftOpp][0] == -1:
            print "know nothing"
            move = self.blindEVplay(game,ev)
        elif game.activePlayers == 2:
            print "Only playing one other person and know his EV"
            if ev > OppEvs[game.rightOpp][0]-OppEvs[game.rightOpp][1]/2 and ev > OppEvs[game.leftOpp][0]-OppEvs[game.leftOpp][1]/2:
                print "know we're better"
                move = self.bestEVplay(game)
            else:
                print "know we're worse"
                move = Move(CHECK)
        elif OppEvs[game.rightOpp][0] == -1 or OppEvs[game.leftOpp][0] == -1:
            print "know only one"
            move = self.blindEVplay(game,ev)
            if OppEvs[game.rightOpp][0]-OppEvs[game.rightOpp][1]/2>ev or OppEvs[game.leftOpp][0]-OppEvs[game.leftOpp][1]/2>ev:
                print "and we're worse than the one we know"
                move = Move(CHECK)
        elif ev > OppEvs[game.rightOpp][0]-OppEvs[game.rightOpp][1]/2 and ev > OppEvs[game.leftOpp][0]-OppEvs[game.leftOpp][1]/2:
            print "know both and we're better"
            move = self.bestEVplay(game)
        else:
            print "know both and we're worse than at least one"
            move = Move(CHECK)

        if ACTION_TYPES[move.type] not in [la[0] for la in game.legalActions]:
            print "returned illegal action"
            move = Move(CHECK)

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
