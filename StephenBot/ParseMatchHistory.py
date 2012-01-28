class ParseMatchHistory():
    def __init__(self, numHand):
        self.packets = []
        self.numHands = numHand
        self.myPlayer = "PoKerboT"
        self.leftOpp = ""
        self.rightOpp = "0"

        self.handID = 0
        self.makingHandPacket = False
        self.firstTie = False
        self.bankrolls = {}
        self.pockets = {}
        self.numLastActions = 0
        self.lastActions = " "
        self.potSize = 0
        self.numBoardCards = 0
        self.boardCards = ""
        self.numLegActions = 0


    def parseHistory(self, h):
        f = open(h, 'r')
        l = f.readline()
        line = l.split(" ")
        if line[0] == "6.S912":
            if line[4] == self.myPlayer:
                self.rightOpp = line[8][:-1] #chop newline
                self.leftOpp = line[6]
            elif line[6] == self.myPlayer:
                self.rightOpp = line[4]
                self.leftOpp = line[8][:-1] #chop newline
            else: #"PoKerboT" == line[8]
                self.rightOpp = line[6]
                self.leftOpp = line[4]
            packet = "NEWGAME 1 "+self.leftOpp+" " + self.rightOpp + " " + str(self.numHands) + " 200 2 1 10000.0000"
            self.packets += [[packet, [], []]]

        self.handID = 0
        self.makingHandPacket = False
        self.firstTie = False
        self.bankrolls = {}
        self.pockets = {}
        self.numLastActions = 0
        self.lastActions = " "
        self.potSize = 0
        self.numBoardCards = 0
        self.boardCards = ""
        self.numLegActions = 0

        l = f.readline()
        while l:
            if l=="\n":
                packet = "HANDOVER "+self.bankrolls[self.myPlayer] + " "+self.bankrolls[self.leftOpp] + " " + self.bankrolls[self.rightOpp] + " "+str(self.numLastActions) + self.lastActions[:-1] + " " + str(self.numBoardCards) + self.boardCards+ " 1000.000"
                self.packets += [[packet, self.pockets[self.leftOpp], self.pockets[self.rightOpp]]]
                l = f.readline()
                continue

            line = l[:-1].split(" ")
            if line[0] == "Hand":
                self.makingHandPacket = True
                self.handID += 1
                self.lastActions = " "
                self.numLastActions = 0
                self.numBoardCards = 0
                self.boardCards = ""
                l = f.readline()
                continue
            elif line[0] == "Seat":
                self.bankrolls[line[3][:-4]] = line[-1]
                if line[3][:-4] == self.myPlayer:
                    self.position = str(int(line[1])-1)
                l = f.readline()
                continue
            elif line[0] == "Dealt":
                self.pockets[line[2][:-4]] = [line[3][1:], line[4][:-1]]
                l = f.readline()
                continue
            elif line[0] == "***":
                self.lastActions += "DEAL:" + line[1] + ","
                self.numLastActions += 1
                if line[1] == "FLOP":
                    self.numBoardCards = 3
                    self.boardCards = " " + line[3][1:] + "," + line[4] + "," + line[5][:-1]
                elif line[1] == "TURN":
                    self.numBoardCards = 4
                    self.boardCards += ","+ line[6][1]+line[6][2]
                elif line[1] == "RIVER":
                    self.numBoardCards = 5
                    self.boardCards += ","+line[7][1]+line[7][2]
                l = f.readline()
                continue
            elif line[0][:-4] in [self.leftOpp, self.rightOpp, self.myPlayer]:
                if line[1] == "posts":
                    self.lastActions += "POST:"+line[0][:-4]+":"+line[-1]+","
                    self.numLastActions += 1
                elif self.makingHandPacket:
                    packet = "NEWHAND "+str(self.handID)+" "+self.position+" "+self.pockets[self.myPlayer][0] + " " + self.pockets[self.myPlayer][1] + " " + self.bankrolls[self.myPlayer] + " " + self.bankrolls[self.leftOpp] + " " +self.bankrolls[self.rightOpp] + " 1000.000"
                    self.packets += [[packet, self.pockets[self.leftOpp], self.pockets[self.rightOpp]]]
                    self.makingHandPacket = False
#                    l = f.readline()
                    continue
                elif line[0][:-4] == self.myPlayer:
                    if line[1] == "wins":
                        self.lastActions += "WIN:"+line[0][:-4]+":"+line[-1][1:-1]+","
                        self.numLastActions +=1
                        l = f.readline()
                        continue
                    elif line[1] == "ties":
                        self.lastActions += "TIE:"+line[0][:-4]+":"+line[-1][1:-1]
                        self.numLastActions+=1
                        self.lastActions += ","
                        l = f.readline()
                        continue
                    elif line[1] == "shows":
                        self.lastActions += "SHOWS:"+line[0][:-4]+":"+self.pockets[line[0][:-4]][0]+":"+self.pockets[line[0][:-4]][1]+","
                        self.numLastActions += 1
                        l = f.readline()
                        continue
                    packet = "GETACTION "+str(self.potSize) + " " +str(self.numBoardCards)+ self.boardCards + " " + str(self.numLastActions)+ self.lastActions[:-1] +" 1 FOLD 10000.0000"
                    self.packets += [[packet, self.pockets[self.leftOpp], self.pockets[self.rightOpp]]]
                    self.numLastActions = 0
                    if line[1] == "folds":
                        self.lastActions = " FOLD:" + self.myPlayer + ","
                        self.numLastActions += 1
                    elif line[1] == "raises":
                        self.lastActions = " RAISE:" + self.myPlayer + ":" + line[-1]+ ","
                        self.numLastActions += 1
                    elif line[1] == "bets":
                        self.lastActions = " BET:" + self.myPlayer + ":" +line[-1]+","
                        self.numLastActions += 1
                    elif line[1] == "calls":
                        self.lastActions = " CALL:" + self.myPlayer + ","
                        self.numLastActions += 1
                    elif line[1] == "checks":
                        self.lastActions = " CHECK:" + self.myPlayer + ","
                        self.numLastActions += 1
                else:
                    if line[1] == "folds":
                        self.lastActions += "FOLD:" + line[0][:-4] + ","
                        self.numLastActions += 1
                    elif line[1] == "raises":
                        self.lastActions += "RAISE:" + line[0][:-4] + ":" + line[-1] + ","
                        self.numLastActions += 1
                    elif line[1] == "bets":
                        self.lastActions += "BET:" + line[0][:-4] + ":" + line[-1] + ","
                        self.numLastActions += 1
                    elif line[1] == "calls":
                        self.lastActions += "CALL:" + line[0][:-4] + ","
                        self.numLastActions += 1
                    elif line[1] == "checks":
                        self.lastActions += "CHECK:" + line[0][:-4] +","
                        self.numLastActions += 1
                    elif line[1] == "shows":
                        self.lastActions += "SHOWS:"+line[0][:-4]+":"+self.pockets[line[0][:-4]][0]+":"+self.pockets[line[0][:-4]][1]+","
                        self.numLastActions += 1
                    elif line[1] == "wins":
                        self.lastActions += "WIN:"+line[0][:-4]+":"+line[-1][1:-1]+","
                        self.numLastActions +=1
                    elif line[1] == "ties":
                        self.lastActions += "TIE:"+line[0][:-4]+":"+line[-1][1:-1]
                        self.numLastActions+=1
                        self.lastActions += ","
                l = f.readline()
                continue

            l = f.readline()
        #for p in self.packets:
        #    print p
        f.close()
