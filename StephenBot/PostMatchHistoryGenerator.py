import sys

from PostMatchHistory import *
from ParseMatchHistory import *

from Enums import *
from GameState import *
from Move import *
from Card import *

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



        

if __name__== "__main__":
    p = PostMatchHistoryGenerator(sys.argv[1])
    p.run()
    p.archive.printHistory()
        
