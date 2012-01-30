import sys

from PostMatchHistory import *
from ParseMatchHistory import *

from Enums import *
from GameState import *
from Move import *
from Card import *

from mpl_toolkits.mplot3d import *
import matplotlib.pyplot as plt

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
        fig = plt.figure()
        ax = Axes3D(fig)
        amt = {}
        for a in self.archive.history[self.game.leftOpp.name][0][CALL]:
#            print a.amount, amt.keys(), a.ev
            if a.amount not in amt.keys():
                amt[a.amount] = {}
            if a.ev[0] not in amt[a.amount].keys():
                amt[a.amount][a.ev[0]] = 0
            amt[a.amount][a.ev[0]] += 1
        xyz = []
        for x in amt.keys():
            for y in amt[x].keys():
                xyz += [[x,y,amt[x][y]]]
        print xyz
        xs = [i[0] for i in xyz]
        ys = [i[1] for i in xyz]
        zs = [i[2] for i in xyz]
        
        ax.scatter(xs,ys,zs)
        ax.set_xlabel("CALL Amount")
        ax.set_ylabel("Hand strength")
        ax.set_zlabel("frequency")
        plt.show()



        

if __name__== "__main__":
    p = PostMatchHistoryGenerator(sys.argv[1])
    p.run()
#    p.archive.printHistory()
    p.plotBets()
        
