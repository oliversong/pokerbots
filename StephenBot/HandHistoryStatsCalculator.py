from ParseMatchHistory import *

import sys,os

from Enums import *
from GameState import *
from ChuckTestaStrat import *
from MatchHistory import *
from PlotBankrolls import *
from Move import *
from Card import *

class HandHistoryRePlayer:
    def __init__(self, fileName):
        self.holeCard1 = None
        self.holeCard2 = None
        self.game = GameState()
        self.archive = MatchHistory()
        self.strategy = ChuckTestaStrat()
        self.history = ParseMatchHistory(1000)
        self.fileName = fileName
        self.history.parseHistory(fileName)

    def run(self):
        statFileName = "stats_normalized.txt"
#        if os.path.exists(statFileName):
#            print statFileName, "already exists, exiting!"
#            return
        f_in = open(self.fileName, 'r')
        f_out = open("stats_normalized.txt", 'a')
        self.history.packets.reverse()
        data = self.history.packets.pop()
        self.run_player(data[0] + "\n")
        for l in f_in.readlines():
            line = l.split(" ")
            if line[0] == "Hand":
                data = self.history.packets.pop()
                self.run_player(data[0]+"\n")
            elif line[0][:-4] == self.history.myPlayer:
                if line[1] in ["posts", "shows", 'ties', 'wins']:
                    pass
                else:
                    data = self.history.packets.pop()
                    if data[0].split(" ")[0] == "GETACTION":
                        move = self.run_player(data[0]+ "\n")
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
                self.run_player(data[0]+"\n")
                if self.game.handID == 1000:
                    f_out.flush()
                    for p in [self.game.leftOpp, self.game.rightOpp]:
                        for s in [0,1,2,3]:
#                            p.aggFreq[s] = float(p.numBets[s])/self.game.handID
#                            p.avgChips[s] = float(p.amountContributed[s])/self.game.handID
#                            if p.numBets[s] >0:
#                                p.avgRaiseAmt[s] = float(p.amountBetRaise[s])/p.numBets[s]

                            l = p.name + " street: "+ str(s)+  " aggFreq: "+ str(p.aggFreq[s])+ " avgChips: "+ str(p.avgChips[s])+ " avgRaiseAmt: "+ str(p.avgRaiseAmt[s]) + "\n"
                            f_out.write(l)
                            f_out.flush()
                    f_out.write("\n")
                    f_out.flush()  
        f_in.close()
        f_out.close()


    def run_player(self,data):
        # Here is where you should implement code to parse the packets from
        # the engine and act on it.
        print "Received", data[:-1]
        self.game.parseInput(data)

        if self.game.state == NEWGAME:
            self.archive.reset(self.game)
        elif self.game.state == GETACTION:
            #self.strategy.evaluateOdds(self.game)
            move = self.strategy.getMove(self.game, self.archive)
#            print "our move:",move
            return move
#        elif self.game.state == HANDOVER:
            #update hand history now that final hand actions have been parsed
#            self.archive.update(self.game)
            #print self.archive
            #self.plot.addMoreBanks(self.game.bankroll, self.game.leftBank,
            #                       self.game.rightBank)
#            print ""
            #if self.game.handID == self.game.numHands:
            #    self.plot.leftOpp = self.game.leftOpp
            #    self.plot.rightOpp = self.game.rightOpp
            #    print "Final time: ", self.game.timebank
            #    print "GAMEOVER PLOTTING"
            #    self.plot.plotBanks()

if __name__ == "__main__":
    p = HandHistoryRePlayer(sys.argv[1])
    p.run()
