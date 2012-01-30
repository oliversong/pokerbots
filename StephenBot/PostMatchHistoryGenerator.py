import sys

from PostMatchHistory import *
from ParseMatchHistory import *

from Enums import *
from GameState import *
from Move import *
from Card import *

#from mpl_toolkits.mplot3d import *
import matplotlib.pyplot as plt
import numpy

class PostMatchHistoryGenerator:
    def __init__(self, fileName):
        self.fileName = fileName
        self.game = GameState()
        self.archive = PostMatchHistory()
        self.history = ParseMatchHistory(1000)

        self.history.parseHistory(fileName)

    def run(self):
        self.history.packets.reverse()

        while len(self.history.packets) > 0:
            data = self.history.packets.pop()

            self.game.parseInput(data[0] + "\n")

            if self.game.state == NEWGAME:
                self.archive.reset(self.game)
            elif self.game.state == HANDOVER:
                self.game.leftOpp.holeCard1 = data[1][0]
                self.game.leftOpp.holeCard2 = data[1][1]
                self.game.rightOpp.holeCard1 = data[2][0]
                self.game.rightOpp.holeCard2 = data[2][1]
                self.archive.update(self.game)

    def plotBets(self):
        #fig = plt.figure()
        for pname in self.archive.history.keys():
            for s in range(RIVER+1):
                #t = RAISE
                for t in self.archive.history[pname][s].keys():
                    #print s,t
                    ys = [int(a.amount) for a in self.archive.history[pname][s][t]]
                    xs = [a.ev[0] for a in self.archive.history[pname][s][t]]
                    if len(xs) == 0 or len(ys) == 0:
                        continue
                    #print xs,ys
                    plt.figure()
                    plt.title(pname)
                    if min(ys) == max(ys):
                        zs = [0 for i in range(1001)]
                        for y in xs:
                            zs[y] += 1
                        x = []
                        y = []
                        for i,z in enumerate(zs):
                            if z>0:
                                x+=[i]
                                y+=[z]
                        plt.scatter(x,y)
                        plt.xlabel("HandStrength")
                        plt.ylabel("Frequency of "+ACTION_TYPES[t]+":"+str(min(ys)))
                    elif min(xs)==max(xs):
                        zs = [0 for i in range(201)]
                        for x in ys:
                            zs[x] += 1
                        x = []
                        y = []
                        for i,z in enumerate(zs):
                            if z>0:
                                x+=[i]
                                y+=[z]
                        plt.scatter(x,y)
                        plt.ylabel("Frequency of EV="+str(min(xs)))
                        plt.xlabel(ACTION_TYPES[t] + ".absAmount")
                    else:
                        plt.hexbin(xs,ys,mincnt=1)
                        plt.axis([0,1000,0,205])
                        plt.xlabel("Hand Strength")
                        plt.ylabel(ACTION_TYPES[t] + ".absAmount")
                        cb = plt.colorbar()
                        cb.set_label('counts')
                    plt.savefig(pname + "-" + STREET_TYPES[s]+"-"+ACTION_TYPES[t] + ".png")

if __name__== "__main__":
    p = PostMatchHistoryGenerator(sys.argv[1])
    p.run()
#    p.archive.printHistory()
    p.plotBets()
