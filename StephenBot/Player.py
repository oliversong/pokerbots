import socket
import sys

from Enums import *
from GameState import *
from LooseAgressiveStrategy import *
from BasicEVStrategy import *
from LagRuleBotStrategy import *
from ChuckTestaStrat import *

class Player:
    def __init__(self, port):
        self.holeCard1 = None
        self.holeCard2 = None
        self.game = GameState()
        self.strategy = None

        self.socket = socket.create_connection(('localhost', port))
        self.fs = socket.makefile()

        self.lag = LooseAgressiveStrategy()
        self.bev = BasicEVStrategy()
        self.lagRule = LagRuleBotStrategy()
        self.chuckTesta = ChuckTestaStrat()

    def run(self):
        while 1:
            # block until the engine sends us a packet
            #data = s.recv(4096)
            data = self.fs.readline()
            # if we receive a null return, then the connection is dead
            if not data:
                print "Gameover, engine disconnected"
                break
            # Here is where you should implement code to parse the packets from
            # the engine and act on it.
            print "Received", data
            self.game.parseInput(data)

            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious packets you send.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, you need to have a newline character (\n) or
            # carriage return (\r), or else your bot will hang!

            if self.game.state == NEWHAND:
                self.setHoleCards(Card(self.game.holeCard1), Card(self.game.holeCard2))
                self.strategy = lagRule

            if self.game.state == GETACTION:
                self.evaluateOdds()
                move = self.makeMove()
                print "SENDING A ", move, "ACTION TO ENGINE\n"
                self.socket.send(move+'\n')
        # if we get here, the server disconnected us, so clean up the socket
        self.socket.close()

    def evaluateOdds(self):
        return self.strategy.evaluateOdds(self)
    def makeMove(self):
        return self.strategy.getMove(self)

    def isValidMove(self, move):
        return false

    def setHoleCards(self, c1, c2):
        self.holeCard1 = c1
        self.holeCard2 = c2
       # self.evaluateHandQualities()

if __name__ == "__main__":
    # port number specified by the engine to connect to.
    port = int(sys.argv[1])
    p = Player(port)
    p.run()
