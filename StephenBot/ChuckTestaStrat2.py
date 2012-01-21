from Strategy import *
from Enums import *

class ChuckTestaStrat2(Strategy):
    def __init__(self):
        Strategy.__init__(self)
        self.numPushMin = 0

    def evaluateOdds(self, b):
        self.evaluatePocketCards(b)
        self.evalHand(b, b.state.boardCards)

    def getMove(self, b):

        ev = self.evalHand(b, b.state.boardCards)
        OppEvs = self.getOppEvs(b)
        
        pos = b.state.position
        move = "CHECK"

#        if b.state.street()==PREFLOP:

        print "RIGHT EV:", OppEvs[b.state.rightOpp], "LEFT EV:", OppEvs[b.state.leftOpp], "EV:", ev

        if OppEvs[b.state.rightOpp][0] == -1 and OppEvs[b.state.leftOpp][0] == -1:
            move = self.blindEVplay(b,ev)
        elif ev > OppEvs[b.state.rightOpp][0]-OppEvs[b.state.rightOpp][1]/2 and ev > OppEvs[b.state.leftOpp][0]-OppEvs[b.state.leftOpp][1]/2:
            move = self.bestEVplay(b,ev)
        elif OppEvs[b.state.rightOpp][0] == -1 or OppEvs[b.state.leftOpp][0] == -1:
            move = self.blindEVplay(b,ev)
            if OppEvs[b.state.rightOpp][0]-OppEvs[b.state.rightOpp][1]/2>ev or OppEvs[b.state.leftOpp][0]-OppEvs[b.state.leftOpp][1]/2>ev:
                move = "CHECK"
        else:
            move = "CHECK"

        if move.split(":")[0] not in [la[0] for la in b.state.legalActions]:
            move = "CHECK"

        return move


    def getOppEvs(self, b):
        OM = self.OppMoves(b)
        OppEvs = {}
        OppEvs[b.state.rightOpp] = [-1,-1]
        OppEvs[b.state.leftOpp] = [-1,-1]


        if len(OM[b.state.rightOpp]) == 0:
            OppEvs[b.state.rightOpp] = [-1,-1]
            print ("No Previous Move on right")
        elif OM[b.state.rightOpp][-1][1].type == FOLD:
            OppEvs[b.state.rightOpp] = [0,-1]            
        elif OM[b.state.rightOpp][-1][1].type == CHECK:
            OppEvs[b.state.rightOpp] = b.state.matchHistory.averageStrength(b.state.rightOpp,
                                                                  OM[b.state.rightOpp][-1][0],
                                                                  OM[b.state.rightOpp][-1][1].type,
                                                                  ABSAMOUNT,
                                                                  OM[b.state.rightOpp][-1][1].amount-200,
                                                                  OM[b.state.rightOpp][-1][1].amount+200)
        elif OM[b.state.rightOpp][-1][1].type in [BET, RAISE]:    
            absamt = b.state.matchHistory.averageStrength(b.state.rightOpp,
                                                                  OM[b.state.rightOpp][-1][0],
                                                                  OM[b.state.rightOpp][-1][1].type,
                                                                  ABSAMOUNT,
                                                                  OM[b.state.rightOpp][-1][1].amount-10,
                                                                  OM[b.state.rightOpp][-1][1].amount+10)   
            betamt = b.state.matchHistory.averageStrength(b.state.rightOpp,
                                                                  OM[b.state.rightOpp][-1][0],
                                                                  OM[b.state.rightOpp][-1][1].type,
                                                                  BETAMOUNT,
                                                                  OM[b.state.rightOpp][-1][2]-1,
                                                                  OM[b.state.rightOpp][-1][2]+1)
            if absamt[1]<betamt[1]:
                OppEvs[b.state.rightOpp] = absamt
                print"Abs Amount EV for Right"
            else:
                OppEvs[b.state.rightOpp] = betamt
                print"Bet Amt EV for Right", betamt[0]
                print  OM[b.state.rightOpp][-1][2]
        elif OM[b.state.rightOpp][-1][1].type == CALL:
            OppEvs[b.state.rightOpp] = b.state.matchHistory.averageStrength(b.state.rightOpp,
                                                                  OM[b.state.rightOpp][-1][0],
                                                                  OM[b.state.rightOpp][-1][1].type,
                                                                  ABSAMOUNT,
                                                                  OM[b.state.rightOpp][-1][1].amount-10,
                                                                  OM[b.state.rightOpp][-1][1].amount+10)
        else:
            print "getOppEvs is broken", OM[b.state.leftOpp][-1][1].type


        if len(OM[b.state.leftOpp]) ==0:
            OppEvs[b.state.leftOpp] = [-1,-1]
            print "No previous move on left"
        elif OM[b.state.leftOpp][-1][1].type == FOLD:
            OppEvs[b.state.leftOpp] = [0,-1]            
        elif OM[b.state.leftOpp][-1][1].type == CHECK:
            OppEvs[b.state.leftOpp] = b.state.matchHistory.averageStrength(b.state.leftOpp,
                                                                  OM[b.state.leftOpp][-1][0],
                                                                  OM[b.state.leftOpp][-1][1].type,
                                                                  ABSAMOUNT,
                                                                  OM[b.state.leftOpp][-1][1].amount-200,
                                                                  OM[b.state.leftOpp][-1][1].amount+200)
        elif OM[b.state.leftOpp][-1][1].type in [BET, RAISE]:    
            absamt = b.state.matchHistory.averageStrength(b.state.leftOpp,
                                                                  OM[b.state.leftOpp][-1][0],
                                                                  OM[b.state.leftOpp][-1][1].type,
                                                                  ABSAMOUNT,
                                                                  OM[b.state.leftOpp][-1][1].amount-10,
                                                                  OM[b.state.leftOpp][-1][1].amount+10)   
            betamt = b.state.matchHistory.averageStrength(b.state.leftOpp,
                                                                  OM[b.state.leftOpp][-1][0],
                                                                  OM[b.state.leftOpp][-1][1].type,
                                                                  BETAMOUNT,
                                                                  OM[b.state.leftOpp][-1][2]-1,
                                                                  OM[b.state.leftOpp][-1][2]+1)
            if absamt[1]<betamt[1]:
                OppEvs[b.state.leftOpp] = absamt
            else:
                OppEvs[b.state.leftOpp] = betamt
        elif OM[b.state.leftOpp][-1][1].type == CALL:
            OppEvs[b.state.leftOpp] = b.state.matchHistory.averageStrength(b.state.leftOpp,
                                                                  OM[b.state.leftOpp][-1][0],
                                                                  OM[b.state.leftOpp][-1][1].type,
                                                                  ABSAMOUNT,
                                                                  OM[b.state.leftOpp][-1][1].amount-10,
                                                                  OM[b.state.leftOpp][-1][1].amount+10)
        else:
            print "getOppEvs is broken", OM[b.state.leftOpp][-1][1].type
   


        return OppEvs

    def OppMoves(self, b):
        OM = {}
        OM[b.state.rightOpp]=[]
        OM[b.state.leftOpp] =[]
        st = 0 #Are there 3 DEAL actions at the beginning of the game?
                #I want st = 0 during the PREFLOP
        prevbet = 2
        
        for acts in b.state.hand.actions:
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
                else:
                    print "ERRROR IN OPPMOVES"
                if acts.player == b.state.rightOpp:
                    OM[b.state.rightOpp] += [(st,acts,betperc)] 
                if acts.player == b.state.leftOpp:
                    OM[b.state.leftOpp] += [(st,acts,betperc)] 

        return OM


    def get_allIn(self,b):
        st = -3
        bets = [0,0,0,0]
        prevBet = 0
        allinbet = 200
        for acts in b.state.hand.actions:
            if acts.type == DEAL:
                st+=1
                prevBet = 0
            elif acts.player != b.state.rightOpp and acts.player!= b.state.leftOpp and acts.type in [CALL, BET, RAISE, POST]: #Want to say acts.player == b.state.myName what is the field name for our name?
                if acts.type == CALL:
                    bets[st] = prevBet
                elif acts.type == POST:
                    bets[0] = acts.amount
                else:
                    bets[st] = acts.amount
                    
            if acts.type in [BET, RAISE, POST]:
                preBet = acts.amount

        if st>0:
            for i in range(st-1):
                allinbet -= bets[i]

        return allinbet
            
            

    def blindEVplay(self, b, ev):
        move = "CHECK"
        if ev>400:
            move = self.pushMin(b,10)
            if move.split(":")[0] in [BET, RAISE]:
                if int(move.split(":")[1]) > 50:
                    move = "CALL"
        elif ev>300:
            move = self.pushMin(b,4)
            if move.split(":")[0] in [BET, RAISE]:
                if int(move.split(":")[1]) > 50:
                    move = "CALL"
        else:
            move =  self.maxRisk(b,2)

#        print "BLIND EV PLAY:", move
        return move


    def bestEVplay(self, b, ev):
        move = self.pushMin(b,5)
        if move.split(":")[0] in [BET, RAISE]:
            if int(move.split(":")[1]) > 50:
                move = "CALL"
#        print "BEST EV PLAY:", move
        return move


    #Bet or raise the minimum amount, or times some multiplier def pushMin(self, b, m=1):
    def pushMin(self, b, m=1):
        self.numPushMin += 1
#        print "PUSH MIN:", self.numPushMin
        if "BET" in [la[0] for la in b.state.legalActions]:
            move = "BET"+":"+str(int(min(self.get_allIn(b),int(la[1])*m)))
        elif "RAISE" in [la[0] for la in b.state.legalActions]:
            move= "RAISE"+":"+str(int(min(self.get_allIn(b),int(la[1])*m)))
        else:
            move = "CALL"

	
        print "PUSH MIN MOVE:", move
        return move #CHECK LOGIC FOR THIS FUCNTION, SHOULD NEVER GET HERE

    ##If can check, then check. Otherwise call up to m
    def maxRisk(self, b, m):
        if "CHECK" in [la[0] for la in b.state.legalActions]:
            return "CHECK"
        if b.state.lastBet <= m:
            return "CALL"
        return "FOLD"

        

        
