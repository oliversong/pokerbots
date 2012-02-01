import socket
import sys

from Enums import *
from GameState import *
from LagRuleBotStrategy import *
from MatchHistory import *
from PlotBankrolls import *
from Move import *

class Player:
    def __init__(self, port):
        self.holeCard1 = None
        self.holeCard2 = None
        self.startBank = None
        self.game = GameState()
        self.players = {}
        self.strategy = Strategy()
        self.losingStrat = LagRuleBotStrategy()
        self.winningStrat = LagRuleBotStrategy()
        self.plot = PlotBankrolls()
        while True:
            try:
                self.socket = socket.create_connection(('localhost', port))
            except socket.error, msg:
                continue
            else:
                break
        self.fs = self.socket.makefile()

    def run(self):
        while 1:
            # block until the engine sends us a packet
            data = self.fs.readline()
            # if we receive a null return, then the connection is dead
            if not data:
                print "Gameover, engine disconnected"
                break
            # Here is where you should implement code to parse the packets from
            # the engine and act on it.
            print "Received", data[:-1]
            self.game.parseInput(data)

            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious packets you send.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, you need to have a newline character (\n) or
            # carriage return (\r), or else your bot will hang!
            if self.game.timebank<0:
                print "OUT OF TIME. current time: ", self.game.timebank," at hand:", self.game.handID

            if self.game.state == NEWGAME:
                if self.game.leftOpp.name not in self.players.keys():
                    self.players[self.game.leftOpp.name] = self.game.leftOpp
                else:
                    self.game.leftOpp = self.players[self.game.leftOpp.name]
                if self.game.rightOpp.name not in self.players.keys():
                    self.players[self.game.rightOpp.name] = self.game.rightOpp
                else:
                    self.game.rightOpp = self.players[self.game.rightOpp.name]

                self.game.leftOpp.newGame()
                self.game.rightOpp.newGame()

                self.startBank = None
            elif self.game.state == NEWHAND:
                if self.startBank is None:
                    self.startBank = self.game.me.bankroll
                    self.strategy = self.winningStrat
                elif self.game.me.bankroll < self.startBank - 2000:
                    print "We're losing, using losing strategy!"
                    self.strategy = self.losingStrat
                elif self.game.me.bankroll > self.startBank:
                    print "We're winning, using winning strategy!"
                    self.strategy = self.winningStrat
            elif self.game.state == GETACTION:
                #self.strategy.evaluateOdds(self.game)
                move = self.strategy.getMove(self.game)
                print "our move:",move
                self.socket.send(move.toString())
            elif self.game.state == HANDOVER:
                self.plot.addMoreBanks(self.game.me.bankroll,
                                       self.game.leftOpp.bankroll,
                                       self.game.rightOpp.bankroll)
                print ""
                if self.game.handID == self.game.numHands:
                    self.plot.leftOpp = self.game.leftOpp.name
                    self.plot.rightOpp = self.game.rightOpp.name
                    print "Final time: ", self.game.timebank
                    print "GAMEOVER PLOTTING"
                    self.plot.plotBanks()
        # if we get here, the server disconnected us, so clean up the socket
        self.socket.close()

if __name__ == "__main__":
    # port number specified by the engine to connect to.
    port = int(sys.argv[1])
    p = Player(port)
    p.run()
