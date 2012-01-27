from Card import *
from Enums import *
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

        self.hand = Hand()
        #self.trackedHands = [CHECK,BET,RAISE,CALL, POST]

    def resetHand(self):
        self.handID = None
        # position: 0=dealer, 1=sb, 2=bb
        self.position = None
        self.holeCard1 = None
        self.holeCard2 = None
        self.bankroll = None
        self.leftBank = None
        self.rightBank = None

        self.potSize = None
        self.pot = 0
        self.numBoardCards = None

        self.boardCards = "__,__,__,__,__"#["__","__","__","__","__"]
        self.numLastActions = None
        self.lastActions = None
        self.numLegalActions = None
        self.legalActions = None

        self.hand.clearHand()

        self.stacks = [self.stackSize]*3
        self.pips = [0]*3
        self.lastBet = 0
        self.street = PREFLOP
        self.activePlayers = 3

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

        elif self.state == NEWHAND:
            self.resetHand()

            self.handID = int(packet[1])
            self.position = int(packet[2])
            self.holeCard1 = Card(packet[3])
            self.holeCard2 = Card(packet[4])
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
                numOptArgs += 1
                self.lastActions = packet[5]
            self.numBoardCards = int(packet[5+numOptArgs])
            if self.numBoardCards>0:
                numOptArgs += 1
                self.boardCards = packet[5+numOptArgs]    #Card(packet[3+i])
            self.timebank = float(packet[-1])

            self.parseBoardCards()
            self.parseLastActions()
            self.hand.splitActionsList()

##            print "bankroll", self.bankroll
##            print "leftbank", self.leftBank
##            print "rightBank", self.rightBank, "\n"

    def parseLastActions(self):
        if self.lastActions:
            self.lastActions = self.lastActions.split(",")
            for i in range(self.numLastActions):
                self.lastActions[i] = self.lastActions[i].split(":")
                #add each action into structure, Hand

                c1 = None
                c2 = None

                sla = self.lastActions[i][0]
                actor = self.lastActions[i][1]
                if actor == self.leftOpp:
                    player = LEFTOPP
                elif actor == self.rightOpp:
                    player = RIGHTOPP
                else:
                    player = ME
                potamt = 0
                betamt = 0
                amt = self.lastBet
                if len(self.lastActions[i]) == 3:
                    amt = float(self.lastActions[i][2])

                if sla == "RAISE":
                    betamt = amt/float(self.lastBet)
                    potamt = amt/float(self.pot + sum(self.pips))
                    self.lastBet = amt
                    self.stacks[player] -= amt - self.pips[player]
                    self.pips[player] = amt
                elif sla == "CALL":
                    betamt = 1.0
                    potamt = amt/float(self.pot + sum(self.pips))
                    self.stacks[player] -= self.lastBet - self.pips[player]
                    self.pips[player] = self.lastBet
                elif sla == "CHECK":
                    if self.street != PREFLOP:
                        amt = 0
                elif sla == "BET":
                    betamt = amt/float(self.lastBet)
                    potamt = amt/float(self.pot + sum(self.pips))
                    self.lastBet = float(self.lastActions[i][2])
                    self.stacks[player] -= self.lastBet
                    self.pips[player] = self.lastBet
                elif sla == "DEAL":
                    amt = 0
                    self.pot += sum(self.pips)
                    self.pips = [0]*3
                    self.street += 1
                elif sla == "POST":
                    self.lastBet = float(self.lastActions[i][2])
                    self.stacks[player] -= self.lastBet
                    self.pips[player] = self.lastBet
                elif sla == "SHOWS":
                    c1 = self.lastActions[i][2]
                    c2 = self.lastActions[i][3]
                    amt = 0
                elif sla == "FOLD":
                    self.activePlayers -= 1
                #elif sla == "REFUND":
                #elif sla == "TIE":
                #elif sla == "WIN":

                a = Action(ACTION_TYPES.index(sla), self.lastActions[i][1], c1,
                           c2, potamt, betamt, amt)
                self.hand.actions.append(a)
                #print "processed action: " + str(a)
                #print "resulting in: stacks",self.stacks, "and pips", self.pips
#        print "lastActions", self.lastActions

    def parseLegalActions(self):
        if self.legalActions:
            self.legalActions = self.legalActions.split(",")
            for i in range(self.numLegalActions):
                self.legalActions[i] = self.legalActions[i].split(":")

    def parseBoardCards(self):
        if(type(self.boardCards) == type("STRING")):
            self.boardCards = self.boardCards.split(",")
        for i in range(5-len(self.boardCards)):
            self.boardCards += ["__"]

    # Return amount needed to raise/bet all in
    def getAllIn(self):
        return int(self.stacks[ME]+self.pips[ME])
