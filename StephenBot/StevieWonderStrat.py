from Strategy import *
from Enums import *
from Move import *
import random

class StevieWonderStrat(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):
        # Calculate our ev
        ev = self.evalHand(game)
        #if ev <275:
        #    return "CHECK"

        move = self.blindEVplay(game,ev)
        return move

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
