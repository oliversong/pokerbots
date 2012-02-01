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
        annFileName = self.fileName[:-3]+"ann"
        if os.path.exists(annFileName):
            print annFileName, "already exists, exiting!"
            return
        f_in = open(self.fileName, 'r')
        f_out = open(self.fileName[:-3]+"ann", 'w')
        self.history.packets.reverse()
        data = self.history.packets.pop()
        self.processInput(data[0] + "\n")
        for l in f_in.readlines():
            line = l.split(" ")
            if line[0] == "Hand":
                data = self.history.packets.pop()
                self.processInput(data[0] + "\n")
                if int(line[1][1:-1]) != self.game.handID:
                    print line[1], "!=",self.game.handID
            elif line[0][:-4] == self.history.myPlayer:
                if line[1] in ["posts", "shows", 'ties', 'wins']:
                    pass
                else:
                    data = self.history.packets.pop()
                    if data[0].split(" ")[0] == "GETACTION":
                        move = self.processInput(data[0] + "\n")
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
                self.processInput(data[0] + "\n")
            f_out.write(l)
            f_out.flush()
        f_in.close()
        f_out.close()

if __name__ == "__main__":
    p = HandHistoryRePlayer(sys.argv[1])
    p.run()
