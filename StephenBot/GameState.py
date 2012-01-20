from Card import *
from Enums import *
from MatchHistory import *
from Action import *
from Hand import *

class GameState:
    def __init__(self):
        self.state = None
        self.resetGame()
        self.resetHand()

    def resetGame(self):
        self.matchID = None
        self.leftOpp = None
        self.rightOpp = None
        self.numHands = None
        self.stackSize = None
        self.bigB = None
        self.smallB = None
        self.timebank = None
        self.matchHistory = MatchHistory()
       
        self.hand = Hand()
        self.trackedHands = [CHECK,BET,RAISE,CALL, POST]

    def resetHand(self):
#        self.hand.printHand()
        
        self.handID = None
        self.position = None
        self.holeCard1 = None
        self.holeCard2 = None
        self.bankroll = None
        self.leftBank = None
        self.rightBank = None

        self.potSize = None
        self.numBoardCards = None

        self.boardCards = "__,__,__,__,__"#["__","__","__","__","__"]
        self.numLastActions = None
        self.lastActions = None
        self.numLegalActions = None
        self.legalActions = None

        self.hand.clearHand()

        self.lastBet = 0


    def parseInput(self, input):
        numOptArgs = 0
        packet = input.split(" ")
        self.state = packet[0]
        if self.state == NEWGAME:
            self.resetGame()

            self.matchID = int(packet[1])
            self.leftOpp = packet[2]
            self.rightOpp = packet[3]
            self.numHands = int(packet[4])
            self.stackSize = int(packet[5])
            self.bigB = int(packet[6])
            self.smallB = int(packet[7])
            self.timebank = float(packet[8])

            self.matchHistory.history[self.leftOpp] = [{},{},{},{}]
            for a in range(4):#[BET,CALL,CHECK,RAISE]:
                for s in range(4):
                    self.matchHistory.history[self.leftOpp][s][a] = []
            self.matchHistory.history[self.rightOpp] = [{},{},{},{}]
            for a in range(4):#[BET,CALL,CHECK,RAISE]:
                for s in range(4):
                    self.matchHistory.history[self.rightOpp][s][a] = []


        elif self.state == NEWHAND:
            self.resetHand()

            self.handID = int(packet[1])
            self.position = int(packet[2])
            self.holeCard1 = packet[3]      #Card(packet[3])
            self.holeCard2 = packet[4]      #Card(packet[4])
            self.bankroll = int(packet[5])
            self.leftBank = int(packet[6])
            self.rightBank = int(packet[7])
            self.timeBank = float(packet[8])

        elif self.state == GETACTION:
            self.potSize = int(packet[1])
            self.numBoardCards = int(packet[2])
            if self.numBoardCards>0:
                numOptArgs += 1
                self.boardCards = packet[3]    #Card(packet[3+i])
            #parse action
            self.numLastActions = int(packet[3+numOptArgs])
            if self.numLastActions>0:
                numOptArgs += 1
                self.lastActions = packet[3+numOptArgs]
            self.numLegalActions = int(packet[4+numOptArgs])
            if self.numLegalActions > 0:
                self.legalActions = packet[5+numOptArgs]

            self.timebank = float(packet[-1])

            self.parseBoardCards()
            self.parseLastActions()
            self.parseLegalActions()

        elif self.state == HANDOVER:
            self.bankroll = int(packet[1])
            self.leftBank = int(packet[2])
            self.rightBank = int(packet[3])
            self.numLastActions = int(packet[4])
            #parse actions  
            if self.numLastActions>0:
                self.lastActions = packet[5]
            self.timebank = float(packet[-1])

            self.parseLastActions()
            self.hand.splitActionsList()
            
            #update hand history now that final hand actions have been parsed
            self.matchHistory.updateHistory(self, self.hand)

            print "bankroll", self.bankroll
            print "leftbank", self.leftBank
            print "rightBank", self.rightBank, "\n"

#            self.matchHistory.printHistory()
        

    def parseLastActions(self):
        if self.lastActions:
            self.lastActions = self.lastActions.split(",")
            for i in range(self.numLastActions):
                self.lastActions[i] = self.lastActions[i].split(":")
                #add each action into structure, Hand
            
                c1 = None
                c2 = None
            
                t = None
                sla = self.lastActions[i][0]
                if self.lastActions[i][0] == "RAISE":
                    t = RAISE
                    self.lastBet = float(self.lastActions[i][2])
                elif self.lastActions[i][0] == "CALL":
                    t = CALL
                elif self.lastActions[i][0] == "CHECK":
                    t = CHECK
                elif self.lastActions[i][0] == "BET":
                    t = BET
                    self.lastBet = float(self.lastActions[i][2])
                elif self.lastActions[i][0] == "FOLD":
                    t = FOLD
                elif self.lastActions[i][0] == "DEAL":
                    t = DEAL
                    self.lastBet = 0
                elif self.lastActions[i][0] == "POST":
                    t = POST
                    self.lastBet = float(self.lastActions[i][2])
                elif sla == "REFUND":
                    t = REFUND
                elif sla == "SHOWS":
                    c1 = self.lastActions[i][2]
                    c2 = self.lastActions[i][3]
                    t = SHOW
                elif sla == "TIE":
                    t = TIE
                elif sla == "WIN":
                    t = WIN


                a = Action(t, self.lastActions[i][1], c1, c2)
                if t in [RAISE,BET,POST]:            #self.lastActions[i][0] in ["RAISE","BET"]:#[RAISE, BET]:
                    a.amount = float(self.lastActions[i][2])
                elif t == CALL:
                    a.amount = self.lastBet
                self.hand.actions.append(a)
#        print "lastActions", self.lastActions
    
    def parseLegalActions(self):
        if self.legalActions:
            self.legalActions = self.legalActions.split(",")
            for i in range(self.numLegalActions):
                self.legalActions[i] = self.legalActions[i].split(":")
 
    def street(self):
        if self.numBoardCards == 0:
            return PREFLOP
        elif self.numBoardCards == 3:
            return FLOP
        elif self.numBoardCards == 4:
            return TURN
        elif self.numBoardCards == 5:
            return RIVER
        else:
            return None

    def parseBoardCards(self):
        if(type(self.boardCards) == type("STRING")):
            self.boardCards = self.boardCards.split(",")
        for i in range(5-len(self.boardCards)):
            self.boardCards += ["__"]
