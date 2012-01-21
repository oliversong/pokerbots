import socket
import sys

from Enums import *
from GameState import *
from LagRuleBotStrategy import *

class Player:
    def __init__(self, port):
        self.holeCard1 = None
        self.holeCard2 = None
        self.game = GameState()
        self.strategy = LagRuleBotStrategy()
        while True:
            try:
                self.socket = socket.create_connection(('oderby.mit.edu', port))
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
            print "Received", data
            self.game.parseInput(data)

            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious packets you send.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, you need to have a newline character (\n) or
            # carriage return (\r), or else your bot will hang!

            if self.game.state == GETACTION:
                self.strategy.evaluateOdds(self)
                move = self.strategy.getMove(self)
                print "SENDING A ", move, "ACTION TO ENGINE\n"
                self.socket.send(move+'\n')
        # if we get here, the server disconnected us, so clean up the socket
        self.socket.close()

if __name__ == "__main__":
    # port number specified by the engine to connect to.
    port = int(sys.argv[1])
    p = Player(port)
    p.run()
