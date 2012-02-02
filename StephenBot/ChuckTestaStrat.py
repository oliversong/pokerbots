from Strategy import *
from Enums import *
from Move import *
import random

class ChuckTestaStrat(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game):
        # Calculate our ev
        ev = self.evalHand(game)

        OppEvs = self.getOppEvs(game)

        move = Move(CHECK)
        scores = {}
        for pname,p in OppEvs.items():
            if p[0] == -1:
                scores[pname] = UNKNOWN
            elif ev>p[0]+p[1]/2.0:
                scores[pname] = BEST
            elif ev>p[0]-p[1]:
                scores[pname] = OK
            else:
                scores[pname] = BAD

        print "LEFT EV:", OppEvs[game.leftOpp.name],"agg?",game.leftOpp.isAggressive(game),"-",scores[game.leftOpp.name], "RIGHT EV:", OppEvs[game.rightOpp.name],"agg?",game.rightOpp.isAggressive(game),"-",scores[game.rightOpp.name], "EV:", ev, "activePlayers:", game.activePlayers
        comment = ""

        if game.leftOpp.isAggressive(game) and game.rightOpp.isAggressive(game): ##Both opp are aggressive
            comment = "Both opponents are aggressive, "
            if game.activePlayers == 3:
                comment += "3 are playing, "
                move = self.aggPlay3(game,scores[game.rightOpp.name],scores[game.leftOpp.name],ev)
            elif game.activePlayers == 2:
                comment += "2 are playing, "
                player = game.leftOpp
                if not player.active:
                    player = game.rightOpp
                score = scores[player.name]
                move = self.aggPlay2(game,score,ev)
            else:
                comment = "neither 3 nor 2 are playing???", game.activePlayers, "players"
        elif game.leftOpp.isAggressive(game) or game.rightOpp.isAggressive(game): ##One opp is aggressive and one opp is not
            comment = "One opponent is aggressive and one is not, "
            if game.leftOpp.isAggressive(game):
                Aplayer = game.leftOpp
                Uplayer = game.rightOpp
            else:
                Aplayer = game.rightOpp
                Uplayer = game.leftOpp
            if game.activePlayers == 3:
                comment += "3 are playing, "
                if scores[game.rightOpp.name] == UNKNOWN and scores[game.leftOpp.name] == UNKNOWN:
                    comment += "know neither opp's EV, "
                    if Uplayer.lastAction.type in [BET, RAISE]: #Need to Check this
                        comment += "unaggresive player bet or raised, "
                        move = self.blindEVplay(game,ev)
                    else:
                        comment += "unaggressive player did not bet or raise, "
                        move = self.blindAggPlay(game,ev)
                elif scores[game.rightOpp.name] == UNKNOWN or scores[game.leftOpp.name] == UNKNOWN:
                    if scores[Aplayer.name] != UNKNOWN: #We know the agressive player
                        comment += "only know agressive player's EV, "
                        if Uplayer.lastAction.type in [BET, RAISE]: #Need to Check this
                            comment += "unaggresive player bet or raised, "
                            move = self.evPlay3(game,scores[game.rightOpp.name],scores[game.leftOpp.name],ev)
                        else:
                            comment += "unaggressive player did not bet or raise, "
                            move = self.aggPlay3(game,scores[game.rightOpp.name],scores[game.leftOpp.name],ev)
                    else: #We know the unagressive player
                        comment += "only know unaggressive player's EV, "
                        if Uplayer.lastAction.type in [BET, RAISE]: #Need to Check this
                            comment += "unaggresive player bet or raised, "
                            move = self.evPlay3(game,scores[game.rightOpp.name],scores[game.leftOpp.name],ev)
                        else:
                            comment += "unaggressive player did not bet or raise, "
                            move = self.blindAggPlay(game,ev)
                else:
                    "know both EVs, "
                    if Uplayer.lastAction.type in [BET, RAISE]: #Need to Check this
                        comment += "unaggresive player bet or raised, "
                        move = self.evPlay3(game,scores[game.rightOpp.name],scores[game.leftOpp.name],ev)
                    else:
                        comment += "unaggressive player did not bet or raise, "
                        move = self.blindAggPlay(game,ev)
            elif game.activePlayers == 2:
                comment += "2 are playing, "
                player = game.leftOpp
                if not player.active:
                    player = game.rightOpp
                score = scores[player.name]

                if player.isAggressive(game):
                    comment += "aggressive player is still playing"
                    move = self.aggPlay2(game,score,ev)
                else:
                    comment += "unaggressive player is still playing"
                    move = self.evPlay2(game,score.ev)
            else:
                comment = "neither 3 nor 2 are playing???", game.activePlayers, "players"
        else: ##Neither opp is aggressive
            comment += "neither opponent is aggressive, "
            if game.activePlayers == 3:
                comment += "3 are playing"
                move = self.evPlay3(game,scores[game.rightOpp.name],scores[game.leftOpp.name],ev)
            elif game.activePlayers == 2:
                comment += "2 are playing"
                player = game.leftOpp
                if not player.active:
                    player = game.rightOpp
                score = scores[player.name]
                move = self.evPlay2(game,score,ev)
            else:
                comment = "Know Nothing and neither 3 or 2 players in game, there are", game.activePlayers, "players"

        #print comment
        if ACTION_TYPES[move.type] not in [la[0] for la in game.legalActions]:
#            print "returned illegal action",move,"! in",game.legalActions
            move = Move(CHECK)

        move.rightEV = OppEvs[game.rightOpp.name]
        move.leftEV = OppEvs[game.leftOpp.name]
        move.myEV = ev
        move.comment = comment

        return move

    def getOppEvs(self, game):
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

            absamt = p.archive.averageStrength(game, lastAction, ABSAMOUNT)

            if lastAction.type == CHECK:
                OppEvs[p.name] = absamt
                continue

            potamt = p.archive.averageStrength(game, lastAction, POTAMOUNT)

            if lastAction.type in [BET, CALL]:
                OppEvs[p.name] = min(absamt,potamt,key=lambda x:x[1])
            elif lastAction.type == RAISE:
                betamt = p.archive.averageStrength(game, lastAction, BETAMOUNT)
                OppEvs[p.name] = min(absamt,betamt,potamt,key=lambda x:x[1])
        return OppEvs

    def badAggPlay(self, game):
        curAmt = game.lastBet
        potAmt = game.pot + game.rightOpp.pip + game.leftOpp.pip + game.me.pip
        street = game.street

        move = Move(CHECK)

        canBet = False
        canRaise = False
        for la in game.legalActions:
            if la[0] == "BET":
                canBet = True
            if la[0] == "RAISE":
                canRaise = True

        if canRaise and curAmt > 2*potAmt: #don't call super aggressive bets
            #with bad ev
            return move

        if street == PREFLOP:
            move = Move(CHECK)
            #Raise 10% of the time
            if random.randint(1,100) <= 10 and canRaise:
                move = Move(RAISE, random.randint(1,2)*potAmt)
        elif street == FLOP:
            if canRaise:
                move = Move(CHECK)
                if random.randint(1,100) <= 60:
                    move = Move(RAISE, random.randint(20,25)/10.0*game.lastBet)
            elif canBet:
                move = Move(CHECK)
                if random.randint(1,100) <= 35:
                    move = Move(BET, random.randint(33,50)/100.0*potAmt)
        elif street == TURN:
            if canRaise:
                move = Move(CHECK)
                if random.randint(1,100) <= 15:
                    move = Move(RAISE, random.randint(20,25)/10.0*game.lastBet)
            elif canBet:
                move = Move(CHECK)
                if random.randint(1,100) <= 7:
                    move = Move(BET, random.randint(33,50)/100.0*potAmt)

        if move.type == CHECK and curAmt < .33 * potAmt and canRaise:
            move = Move(CALL)
            if random.randint(1,100) <= 50:
                move = Move(RAISE, random.randint(20,25)/10.0*game.lastBet)
        move.amount = min([move.amount, game.me.getAllIn()])
        return move

    def okAggPlay(self,game):
        move = Move(CHECK)
        curAmt = game.lastBet
        potAmt = game.pot + game.rightOpp.pip + game.leftOpp.pip + game.me.pip
        street = game.street

        canBet = False
        canRaise = False
        for la in game.legalActions:
            if la[0] == "BET":
                canBet = True
            if la[0] == "RAISE":
                canRaise = True

        if game.street == PREFLOP:
            if curAmt>50:
                return move
            move = Move(CALL)
            if random.randint(1,100) <= 10 and canRaise:
                move = Move(RAISE, random.randint(1,3)*potAmt)
        elif game.street == FLOP:
            if canRaise:
                move = Move(CALL)
                if random.randint(1,100) <= 75:
                    move = Move(RAISE, random.randint(20,25)/10.0*game.lastBet)
            elif canBet:
                move = Move(CHECK)
                if random.randint(1,100) <= 35:
                    move = Move(BET, random.randint(33,66)/100.0*potAmt)
        elif game.street == TURN:
            if canRaise:
                move = Move(CHECK)
                if random.randint(1,100) <= 45:
                    move = Move(RAISE, random.randint(20,25)/10.0*game.lastBet)
            elif canBet:
                move = Move(CHECK)
                if random.randint(1,100) <= 25:
                    move = Move(BET, random.randint(33,66)/100.0*potAmt)
        elif game.street == RIVER:
            if canRaise:
                move = Move(CHECK)
                if random.randint(1,100) <= 15:
                    move = Move(RAISE, random.randint(20,25)/10.0*game.lastBet)
            elif canBet:
                move = Move(CHECK)
                if random.randint(1,100) <= 15:
                    move = Move(BET, random.randint(33,66)/100.0*potAmt)
        else:
            print "Error! You reached a state not 0-3! in blindEVplay"

        if move.type == CHECK and curAmt < .33 * potAmt and canRaise:
            move = Move(CALL)
            if random.randint(1,100) <= 50:
                move = Move(RAISE, random.randint(20,25)/10.0*game.lastBet)
        move.amount = min([move.amount, game.me.getAllIn()])
        return move

    def goodAggPlay(self,game):
        move = Move(CHECK)
        curAmt = game.lastBet
        potAmt = game.pot + game.rightOpp.pip + game.leftOpp.pip + game.me.pip

        canBet = False
        canRaise = False
        for la in game.legalActions:
            if la[0] == "BET":
                canBet = True
            if la[0] == "RAISE":
                canRaise = True

        if game.street == PREFLOP:
            move = Move(CALL)
            if random.randint(1,100) <= 50 and canRaise:
                move = Move(RAISE, random.randint(1,5)*potAmt)
        elif game.street == FLOP:
            move = Move(CALL)
            if canRaise:
                if random.randint(1,100) <= 50:
                    move = Move(RAISE, random.randint(20,25)/10.0*game.lastBet)
            elif canBet:
                move = Move(CHECK)
                if random.randint(1,100) <= 50:
                    move = Move(BET, random.randint(66,75)/100.0*potAmt)
        elif game.street == TURN:
            move = Move(CALL)
            if canRaise:
                if random.randint(1,100) <= 45:
                    move = Move(RAISE, random.randint(20,25)/10.0*game.lastBet)
            elif canBet:
                move = Move(CHECK)
                if random.randint(1,100) <= 75:
                    move = Move(BET, random.randint(66,75)/100.0*potAmt)
        elif game.street == RIVER:
            move = Move(CALL)
            if canRaise:
                amt = round(min([2.5*game.lastBet, game.me.getAllIn()]))
                move = Move(RAISE, random.randint(amt, round(game.me.getAllIn())))
            elif canBet:
                move = Move(BET, random.randint(50,150)/100.0*potAmt)
        move.amount = min([move.amount, game.me.getAllIn()])
        return move

    def blindAggPlay(self,game,ev):
        street = game.street
        npm = 0

        if street == PREFLOP:
            if game.activePlayers == 2:
                npm = 200
            if ev>450+npm:
                return self.goodAggPlay(game)
            elif ev>325+npm:
                return self.okAggPlay(game)
            elif ev>250+npm:
                return self.maxRisk(game,6)
            return self.maxRisk(game,2)
        elif street == FLOP:
            if game.activePlayers == 2:
                npm = 50
            if ev>800+npm:
                return self.goodAggPlay(game)
            elif ev>670+npm:
                return self.okAggPlay(game)
            elif ev>500+npm:
                return self.badAggPlay(game)
        elif street == TURN:
            if game.activePlayers == 2:
                npm = 70
            if ev>800+npm:
                return self.goodAggPlay(game)
            elif ev>700+npm:
                return self.okAggPlay(game)
            elif ev>600+npm:
                return self.badAggPlay(game)
        elif street == RIVER:
            if game.activePlayers == 2:
                npm = 50
            if ev>850+npm:
                return self.goodAggPlay(game)
            elif ev>780+npm:
                return self.okAggPlay(game)
            else:
                return self.badAggPlay(game)
        else:
            print "Error! You reached a state not 0-3! in blindEVplay"
        return Move(CHECK)

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


    def aggPlay3(self,game,s1,s2,ev):
        if s1 == UNKNOWN and s2 == UNKNOWN:
            return self.blindAggPlay(game,ev)
        elif s1 == BAD or s2 == BAD:
            return self.badAggPlay(game)
        elif s1 == OK or s2 == OK:
            return self.okAggPlay(game)
        else:
            return self.goodAggPlay(game)

    def evPlay3(self,game,s1,s2,ev):
        if s1 == UNKNOWN and s2 == UNKNOWN:
            return self.blindEVplay(game,ev)
        elif s1 == UNKNOWN or s2 == UNKNOWN:
            if s1 == BEST or s2 == BEST:
                return self.bestEVplay(game)
            elif s1 == bad and s2 == bad:
                return Move(CHECK)
            else:
                return self.maxRisk(game,4)
        else:
            if s1 == BEST and s2 == BEST:
                return self.bestEVplay(game)
            elif s1 != BAD and s2 != BAD:
                return self.maxRisk(game,10)
            else:
                return Move(CHECK)

    def aggPlay2(self,game,s1,ev):
        if s1 == UNKNOWN:
            return self.blindAggPlay(game,ev)
        elif s1 == BEST:
            return self.goodAggPlay(game)
        elif s1 == OK:
            return self.okAggPlay(game)
        else:
            return self.badAggPlay(game)

    def evPlay2(self,game,s1,ev):
        if s1 == UNKNOWN:
            return self.blindEVplay(game,ev)
        elif s1 == BEST:
            return self.bestEVplay(game)
        elif s1 == OK:
            return self.maxRisk(game,10)
        else:
            return Move(CHECK)
