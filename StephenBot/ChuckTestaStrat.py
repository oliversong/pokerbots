from Strategy import *
from Enums import *
from Move import *
import random

firstToActCutoffs = [
    [#TAG
        [80, 80, 50],#PREFLOP
        [80, 80, 40],#FLOP
        [80, 80, 40],#TURN
        [80, 70, 0]#RIVER
    ],[#LAP
        [70, 80, 50],#PREFLOP
        [70, 80, 30],#FLOP
        [70, 80, 30],#TURN
        [70, 80, 0]#RIVER
    ]
]

betCutoffs = [
    [#TAG
        [],#PREFLOP - impossible to bet on preflop
        [#FLOP
            [[10, 40], [25, 100], [50, 100]],#BIN1
            [[5,  20], [25, 100], [50, 100]],#BIN2
            [[0,  0 ], [10, 85 ], [40, 100]],#BIN3
            [[0,  0 ], [0,  50 ], [75, 100]] #BIN4
        ],[#TURN
            [[10, 40], [25, 100], [50, 100]],#BIN1
            [[5,  20], [25, 100], [50, 100]],#BIN2
            [[0,  0 ], [10, 85 ], [40, 100]],#BIN3
            [[0,  0 ], [0,  50 ], [75, 100]] #BIN4
        ],[#RIVER
            [[10, 40], [25, 100], [100, 100]],#BIN1
            [[5,  20], [25, 100], [100, 100]],#BIN2
            [[0,  0 ], [10, 85 ], [100, 100]],#BIN3
            [[0,  0 ], [0,  50 ], [100, 100]] #BIN4
        ]
    ],[#LAP
        [],#PREFLOP - impossible to bet on preflop
        [#FLOP
            [[60, 100], [40, 100], [30, 100]],#BIN1
            [[60, 100], [40, 100], [30, 100]],#BIN2
            [[20, 70 ], [50, 100], [30, 100]],#BIN3
            [[0,  20 ], [75, 100], [30, 100]] #BIN4
        ],[#TURN
            [[60, 100], [40, 100], [30, 100]],#BIN1
            [[60, 100], [40, 100], [30, 100]],#BIN2
            [[20, 70 ], [50, 100], [30, 100]],#BIN3
            [[0,  20 ], [75, 100], [30, 100]] #BIN4
        ],[#RIVER
            [[60, 100], [50, 100], [100, 100]],#BIN1
            [[60, 100], [35, 100], [100, 100]],#BIN2
            [[20, 70 ], [15, 100], [100, 100]],#BIN3
            [[0,  20 ], [0,  100], [100, 100]] #BIN4
        ]
    ]
]

raiseCutoffs = [
    [#TAG
        [#PREFLOP
            [[30, 80], [20, 100], [90, 100]],#BIN1
            [[0,  0 ], [0,  70 ], [70, 100]],#BIN2
            [[0,  0 ], [0,  50 ], [65, 100]],#BIN3
            [[0,  0 ], [0,  30 ], [90, 100]]#BIN3
        ],[#FLOP
            [[0, 40], [0, 100], [70, 100]],#BIN1
            [[0, 0 ], [0, 80 ], [40, 100]],#BIN2
            [[0, 0 ], [0, 50 ], [60, 100]] #BIN3
        ],[#TURN
            [[0, 40], [0, 100], [70, 100]],#BIN1
            [[0, 0 ], [0, 80 ], [40, 100]],#BIN2
            [[0, 0 ], [0, 50 ], [60, 100]] #BIN3
        ],[#RIVER
            [[0, 40], [0, 100], [100, 100]],#BIN1
            [[0, 0 ], [0, 80 ], [100, 100]],#BIN2
            [[0, 0 ], [0, 50 ], [  0, 100]] #BIN3
        ]
    ],[#LAP
        [#PREFLOP
            [[75, 100], [60, 100], [85, 100]],#BIN1
            [[0,  35 ], [40, 100], [70, 100]],#BIN2
            [[0,  0  ], [0,  50 ], [50, 100]],#BIN3
            [[0,  0  ], [0,  25 ], [70, 100]]#BIN3
        ],[#FLOP
            [[0,  100], [70, 100], [85, 100]],#BIN1
            [[15, 30 ], [60, 100], [70, 100]],#BIN2
            [[0,  0  ], [50, 50 ], [50, 100]] #BIN3
        ],[#FLOP
            [[0,  100], [70, 100], [85, 100]],#BIN1
            [[15, 30 ], [60, 100], [70, 100]],#BIN2
            [[0,  0  ], [50, 50 ], [50, 100]] #BIN3
        ],[#RIVER
            [[0, 100], [70, 100], [100, 100]],#BIN1
            [[0, 10 ], [0,  100], [100, 100]],#BIN2
            [[0, 0  ], [0,  50 ], [100, 100]] #BIN3
        ]
    ]
]

blindEVs = [[[300,500,650],[550,670,800],[550,700,800],[500,750,850]],
            [[250,370,445],[380,500,650],[300,500,650],[250,400,700]]]

class ChuckTestaStrat(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game):
        OppEvs = self.getOppEvs(game)
        ev = self.evalHand(game, OppEvs)
        scores = {}
        nump = game.activePlayers

        if ev>blindEVs[nump-2][game.street][2]:
            myBlindEV = GOOD
        elif ev>blindEVs[nump-2][game.street][1]:
            myBlindEV = OK
        elif ev>blindEVs[nump-2][game.street][0]:
            myBlindEV = BAD
        else:
            myBlindEV = AWFUL

        for pname,p in OppEvs.items():
            if p[0] == -1:
                scores[pname] = UNKNOWN
            elif ev>p[0]+p[1]:
                scores[pname] = GOOD
            elif ev>p[0]:
                scores[pname] = OK
            elif ev>p[0]-p[1]:
                scores[pname] = BAD
            else:
                scores[pname] = AWFUL

        maxLeftEV = max([myBlindEV,scores[game.leftOpp.name]])
        if OppEvs[game.leftOpp.name][1]<100:
            maxLeftEV = scores[game.leftOpp.name]
        maxRightEV = max([myBlindEV,scores[game.rightOpp.name]])
        if OppEvs[game.rightOpp.name][1]<100:
            maxLeftEV = scores[game.rightOpp.name]

        print "EV:", ev, "myBlindEV:",myBlindEV, "LEFT EV:", OppEvs[game.leftOpp.name],"-",scores[game.leftOpp.name],"=",scores[game.leftOpp.name], "RIGHT EV:", OppEvs[game.rightOpp.name],"=",scores[game.rightOpp.name], "activePlayers:", game.activePlayers
        if nump == 3:
            score = min([maxLeftEV, maxRightEV])
        else:
            score = maxRightEV
            if not game.rightOpp.active:
                score = maxLeftEV


        tagPlaying = ((not game.leftOpp.isLAP(game) and game.leftOpp.active)
                      or (not game.rightOpp.isLAP(game) and game.rightOpp.active))
        comment = ""
        if score == AWFUL:
            move = Move(CHECK)
        else:
            move = self.decide(game, not tagPlaying, score)
            comment += move.comment
        comment += " score: " + str(score)

        if move.amount is not None:
            move.amount = min([move.amount, game.me.getAllIn()])

        if ACTION_TYPES[move.type] not in [la[0] for la in game.legalActions]:
            print "returned illegal action",move.toString()[:-1],"! in",game.legalActions
            if move.type in [BET,RAISE]:
                move = Move(CALL)
            else:
                move = Move(CHECK)

        move.rightEV = OppEvs[game.rightOpp.name]
        move.leftEV = OppEvs[game.leftOpp.name]
        move.myEV = ev
        move.comment = comment
        return move

    def decide(self, game, isLAP, score):
        firstToAct = False
        facingBet = False
        facingRaise = False
        canBet = False
        canRaise = False
        comment = "isLap=" + str(isLAP) + ", "

        for la in game.legalActions:
            if la[0] == "BET":
                canBet = True
            if la[0] == "RAISE":
                canRaise = True

        lastAction = game.lastActor.lastActions[-1]
        if game.street == PREFLOP:
            firstToAct = lastAction.type == POST
        else:
            firstToAct = game.me.pip + game.leftOpp.pip + game.rightOpp.pip == 0

        if not firstToAct:
            facingBet = lastAction.type == BET
        facingRaise = not firstToAct and not facingBet

        if firstToAct: comment += "first to act "
        if facingBet: comment += "facing a bet of " + str(game.lastBet) + " "
        if facingRaise: comment += "facing a raise to " + str(game.lastBet) + " "

        prob = random.randint(1,100)
        totalPot = game.pot + game.me.pip + game.leftOpp.pip + game.rightOpp.pip
        if game.street == PREFLOP:
            if firstToAct:
                check = firstToActCutoffs[isLAP][PREFLOP][score-1]
                if prob <= check:
                    move = Move(CALL)
                else:
                    move = Move(RAISE, 6)
            else:
                bin = self.getRaiseBin(game.street, game.lastActor.lastActions[-1])
                if bin == BIN1:
                    if isLAP:
                        raiseAmt = int(3.5*totalPot)
                    else:
                        raiseAmt = int(2.75* totalPot)
                elif bin == BIN2:
                    if isLAP:
                        raiseAmt = int(2.5*totalPot)
                    else:
                        raiseAmt = int(3*totalPot)
                elif bin == BIN3:
                    raiseAmt = int(2.5*totalPot)
                else:
                    raiseAmt = game.me.getAllIn()

                comment += " bin="+str(bin) + " raiseamnt=" + str(raiseAmt)
                r,c = raiseCutoffs[isLAP][game.street][bin][score-1]
                if prob <= r:
                    move = Move(RAISE, raiseAmt)
                elif prob <= c:
                    move = Move(CALL)
                else:
                    move = Move(FOLD)
        else:
            if isLAP:
                betAmt = .8*totalPot
                raiseAmt = max([3*game.lastBet, int(.75*totalPot)])
            else:
                betAmt = .5*totalPot
                raiseAmt = 3*game.lastBet

            if firstToAct:
                check = firstToActCutoffs[isLAP][game.street][score-1]
                if prob <= check:
                    move = Move(CHECK)
                else:
                    move = Move(BET, betAmt)
            elif facingBet:
                bin = self.getBetBin(game.lastActor.lastActions[-1].potAmount)
                comment += " bin="+str(bin) + " betamnt=" + str(betAmt)
                r,c = betCutoffs[isLAP][game.street][bin][score-1]
                if prob <= r:
                    move = Move(RAISE, raiseAmt)
                elif prob <= c:
                    move = Move(CALL)
                else:
                    move = Move(FOLD)
            else:
                bin = self.getRaiseBin(game.street, game.lastActor.lastActions[-1])
                comment += " bin="+str(bin) + " raiseamnt=" + str(raiseAmt)
                r,c = raiseCutoffs[isLAP][game.street][bin][score-1]
                if prob <= r:
                    move = Move(RAISE, raiseAmt)
                elif prob <= c:
                    move = Move(CALL)
                else:
                    move = Move(FOLD)
        move.comment = comment
        return move

    def getBetBin(self, potRatio):
        if potRatio <= .5:
            return BIN1
        elif potRatio <= 1.0:
            return BIN2
        elif potRatio <= 3.0:
            return BIN3
        else:
            return BIN4

    def getRaiseBin(self, street, action):
        if street == PREFLOP:
            if action.amount <= 12:
                return BIN1
            elif action.amount <= 25:
                return BIN2
            elif action.amount <= 50:
                return BIN3
            else:
                return BIN4
        else:
            betRatio = action.betAmount
            if action.amount > 50:
                return BIN3
            if betRatio <= 3:
                return BIN1
            elif betRatio <=5:
                return BIN2
            else:
                return BIN3

    def matchLastAction(self, game, player, actionTypes):
        lastAction = player.lastActions[-1]
        return lastAction.type in actionTypes and lastAction.street == game.street

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
        if canRaise: #don't re-raise with bad ev
            if game.rightOpp.active and self.matchLastAction(game, game.rightOpp,[RAISE]):
                return move
            elif game.leftOpp.active and self.matchLastAction(game, game.leftOpp,[RAISE]):
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
        potAmt = game.pot + game.rightOpp.pip + game.leftOpp.pip + game.me.pip
        if s1 == UNKNOWN and s2 == UNKNOWN:
            return self.blindEVplay(game,ev)
        elif s1 == UNKNOWN or s2 == UNKNOWN:
            if s1 == BEST or s2 == BEST:
                return self.bestEVplay(game)
            elif s1 == BAD or s2 == BAD:
                return Move(CHECK)
            else:
                return self.maxRisk(game,potAmt/2.0)
        else:
            if s1 == BEST and s2 == BEST:
                return self.bestEVplay(game)
            elif s1 != BAD and s2 != BAD:
                return self.maxRisk(game,potAmt/2.0)
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
            potAmt = game.pot + game.rightOpp.pip + game.leftOpp.pip + game.me.pip
            return self.maxRisk(game,potAmt/2.0)
        else:
            return Move(CHECK)
