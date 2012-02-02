from ParseMatchHistory import *
from ChuckTestaPlayer import ChuckTestaPlayer
from Card import *

import sys,os

class HandHistoryRePlayer(ChuckTestaPlayer):
    def __init__(self, fileName):
        ChuckTestaPlayer.__init__(self, None)
        self.history = ParseMatchHistory(1000)
        self.fileName = fileName
        self.history.parseHistory(fileName)

    def run(self):
        #statFileName = "stats_normalized.txt"
        f_in = open(self.fileName, 'r')
        #f_out = open("stats_normalized.txt", 'a')
        self.history.packets.reverse()
        data = self.history.packets.pop()
        self.processInput(data[0] + "\n")
        for l in f_in.readlines():
            line = l.split(" ")
            if line[0] == "Hand":
                data = self.history.packets.pop()
                self.processInput(data[0]+"\n")
            elif line[0][:-4] == self.history.myPlayer:
                if line[1] in ["posts", "shows", 'ties', 'wins']:
                    pass
                else:
                    data = self.history.packets.pop()
                    if data[0].split(" ")[0] == "GETACTION":
                        move = self.processInput(data[0]+ "\n")
                        h1 = self.game.holeCard1
                        h2 = self.game.holeCard2
                        self.game.holeCard1 = Card(data[1][0])
                        self.game.holeCard2 = Card(data[1][1])
                        leftEV = self.strategy.evalHand(self.game)
                        self.game.holeCard1 = Card(data[2][0])
                        self.game.holeCard2 = Card(data[2][1])
                        rightEV = self.strategy.evalHand(self.game)
                        self.game.holeCard1 = h1
                        self.game.holeCard2 = h2
                        l = l[:-1] + "  my notes:" + str(move)+" trueLeftEV:" + str(leftEV) + " trueRightEV:" + str(rightEV) + "\n"
            elif l == "\n":
                data = self.history.packets.pop()
                self.processInput(data[0]+"\n")
                if self.game.handID == 1000:
                    ret = ""
                    #f_out.flush()
                    for p in [self.game.leftOpp, self.game.rightOpp]:
                        for s in [0,1,2,3]:
                            ret += "%s,%d,%d,%d,%d,%d,%d,"%(p.name, s, self.game.numArrivalsAtStreet[s], p.numArrivalsAtStreet[s], p.numBets[s], p.amountContributed[s], p.amountBetRaise[s])
                            ret += "%f,%f,%f\n" %(p.aggFreq[s],p.avgChips[s],p.avgRaiseAmt[s])
                            #l = p.name + " street: "+ str(s)+ " aggFreq: "+ str(p.aggFreq[s])+ " avgChips: "+ str(p.avgChips[s])+ " avgRaiseAmt: "+ str(p.avgRaiseAmt[s]) + "\n"
                            #f_out.write(l)
                            #f_out.flush()
                    #f_out.write("\n")
                    #f_out.flush()
        f_in.close()
        return ret
        #f_out.close()

if __name__ == "__main__":
    p = HandHistoryRePlayer(sys.argv[1])
    p.run()
