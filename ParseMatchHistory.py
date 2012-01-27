
class ParseMatchHistory():
    def __init__(self, numHand):
        self.packets = []
        self.numHands = numHand
        self.myPlayer = "PoKerboT"

    def parseHistory(self, h):
        f = open(h, 'r')
        l = f.readline()
        line = l.split(" ")
        if line[0] == "6.S912":
            if line[4] == self.myPlayer:
                rightOpp = line[8][:-1] #chop newline
                leftOpp = line[6]
            elif line[6] == self.myPlayer:
                rightOpp = line[4]
                leftOpp = line[8][:-1] #chop newline
            else: #"PoKerboT" == line[8]
                rightOpp = line[6]
                leftOpp = line[4]
            packet = "NEWGAME 1 "+leftOpp+" " + rightOpp + " " + str(self.numHands) + " 2 1 10000.0000"
            self.packets += [packet]

        handID = 0
        makingHandPacket = False
        firstTie = False
        bankrolls = {}
        pockets = {}
        numLastActions = 0
        lastActions = " "
        potSize = 0
        numBoardCards = 0
        boardCards = ""
        numLegActions = 0

        l = f.readline()
        while l:
            if l=="\n":
                packet = "HANDOVER "+bankrolls[self.myPlayer] + " "+bankrolls[leftOpp] + " " + bankrolls[rightOpp] + " "+str(numLastActions) + lastActions[:-1] + " " + str(numBoardCards) + boardCards+ " 1000.000"
                self.packets += [packet]
                l = f.readline()
                continue

            line = l[:-1].split(" ")
            if line[0] == "Hand":
                makingHandPacket = True
                handID += 1
                lastActions = " "
                numLastActions = 0
                numBoardCards = 0
                boardCards = ""
                l = f.readline()
                continue
            elif line[0] == "Seat":
                bankrolls[line[3][:-4]] = line[-1]
                if line[3][:-4] == self.myPlayer:
                    position = str(int(line[1])-1)
                l = f.readline()
                continue
            elif line[0] == "Dealt":
                pockets[line[2][:-4]] = [line[3][1:], line[4][:-1]]
                l = f.readline()
                continue
            elif line[0] == "***":
                lastActions += "DEAL:" + line[1] + ","
                numLastActions += 1
                if line[1] == "FLOP":
                    numBoardCards = 3
                    boardCards = " " + line[3][1:] + "," + line[4] + "," + line[5][:-1]
                elif line[1] == "TURN":
                    numBoardCards = 4
                    boardCards += ","+ line[6][1]+line[6][2]
                elif line[1] == "RIVER":
                    numBoardCards = 5
                    boardCards += ","+line[7][1]+line[7][2]
                l = f.readline()
                continue
            elif line[0][:-4] in [leftOpp, rightOpp, self.myPlayer]:
                if line[1] == "posts":
                    lastActions += "POST:"+line[0][:-4]+":"+line[-1]+","
                    numLastActions += 1
                elif makingHandPacket:
                    packet = "NEWHAND "+str(handID)+" "+position+" "+pockets[self.myPlayer][0] + " " + pockets[self.myPlayer][1] + " " + bankrolls[self.myPlayer] + " " + bankrolls[leftOpp] + " " +bankrolls[rightOpp] + " 1000.000"
                    self.packets += [packet]
                    makingHandPacket = False
#                    l = f.readline()
                    continue
                elif line[0][:-4] == self.myPlayer:
                    if line[1] == "wins":
                        lastActions += "WIN:"+line[0][:-4]+":"+line[-1][1:-1]+","
                        numLastActions +=1
                        l = f.readline()
                        continue
                    elif line[1] == "ties":
                        lastActions += "TIE:"+line[0][:-4]+":"+line[-1][1:-1]
                        numLastActions+=1
                        lastActions += ","
                        l = f.readline()
                        continue
                    elif line[1] == "shows":
                        lastActions += "SHOWS:"+line[0][:-4]+":"+pockets[line[0][:-4]][0]+":"+pockets[line[0][:-4]][1]+","
                        numLastActions += 1
                        l = f.readline()
                        continue
                    packet = "GETACTION "+str(potSize) + " " +str(numBoardCards)+ boardCards + " " + str(numLastActions)+ lastActions[:-1] +" 1 FOLD 10000.0000"
                    self.packets += [packet]
                    numLastActions = 0
                    if line[1] == "folds":
                        lastActions = " FOLD:" + self.myPlayer + ","
                        numLastActions += 1
                    elif line[1] == "raises":
                        lastActions = " RAISE:" + self.myPlayer + ":" + line[-1]+ ","
                        numLastActions += 1
                    elif line[1] == "bets":
                        lastActions = " BET:" + self.myPlayer + ":" +line[-1]+","
                        numLastActions += 1
                    elif line[1] == "calls":
                        lastActions = " CALL:" + self.myPlayer + ","
                        numLastActions += 1
                    elif line[1] == "checks":
                        lastActions = " CHECK:" + self.myPlayer + ","
                        numLastActions += 1
                else:
                    if line[1] == "folds":
                        lastActions += "FOLD:" + line[0][:-4] + ","
                        numLastActions += 1
                    elif line[1] == "raises":
                        lastActions += "RAISE:" + line[0][:-4] + ":" + line[-1] + ","
                        numLastActions += 1
                    elif line[1] == "bets":
                        lastActions += "BET:" + line[0][:-4] + ":" + line[-1] + ","
                        numLastActions += 1
                    elif line[1] == "calls":
                        lastActions += "CALL:" + line[0][:-4] + ","
                        numLastActions += 1
                    elif line[1] == "checks":
                        lastActions += "CHECK:" + line[0][:-4] +","
                        numLastActions += 1
                    elif line[1] == "shows":
                        lastActions += "SHOWS:"+line[0][:-4]+":"+pockets[line[0][:-4]][0]+":"+pockets[line[0][:-4]][1]+","
                        numLastActions += 1
                    elif line[1] == "wins":
                        lastActions += "WIN:"+line[0][:-4]+":"+line[-1][1:-1]+","
                        numLastActions +=1
                    elif line[1] == "ties":
                        lastActions += "TIE:"+line[0][:-4]+":"+line[-1][1:-1]
                        numLastActions+=1
                        lastActions += ","
                l = f.readline()
                continue

            l = f.readline()
        for p in self.packets:
            print p





