import socket
import sys

from Bot import *
from Enums import *
from GameState import *
from LooseAgressiveStrategy import *
from BasicEVStrategy import *
from LagRuleBotStrategy import *
from ChuckTestaStrat import *


class Main:
    def __init__(self, port):
        self.socket = socket.create_connection(('localhost', port))
        self.fs = socket.makefile()

        self.bot = Bot()
        self.game = GameState()
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
            bot.updateState(self.game)

            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious packets you send.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, you need to have a newline character (\n) or
            # carriage return (\r), or else your bot will hang!

            if self.game.state == NEWHAND:
                self.bot.setHoleCards(Card(game.holeCard1), Card(game.holeCard2))
                bot.strategy = lagRule

            if game.state == GETACTION:
                bot.evaluateOdds()
                move = bot.makeMove()
                print "SENDING A ", move, "ACTION TO ENGINE\n"
                self.socket.send(move+'\n')
        # if we get here, the server disconnected us, so clean up the socket
        self.socket.close()


if __name__ == "__main__":
    # port number specified by the engine to connect to.
    port = int(sys.argv[1])
    # connect the socket to the engine
    s = socket.create_connection(('localhost', port))
    fs = s.makefile()

    bot = Bot()
    game = GameState()
    lag = LooseAgressiveStrategy()
    bev = BasicEVStrategy()
    lagRule = LagRuleBotStrategy()
    chuckTesta = ChuckTestaStrat()

    while 1:
        # block until the engine sends us a packet
        #data = s.recv(4096)
        data = fs.readline()
        # if we receive a null return, then the connection is dead
        if not data:
            print "Gameover, engine disconnected"
            break
        # Here is where you should implement code to parse the packets from
        # the engine and act on it.
        print data
        game.parseInput(data)
        bot.updateState(game)

        # When appropriate, reply to the engine with a legal action.
        # The engine will ignore all spurious packets you send.
        # The engine will also check/fold for you if you return an
        # illegal action.
        # When sending responses, you need to have a newline character (\n) or
        # carriage return (\r), or else your bot will hang!

        if game.state=="NEWHAND":
            bot.setHoleCards(Card(game.holeCard1), Card(game.holeCard2))
            bot.strategy = lagRule

        if game.state == "GETACTION":
##            s.send("RAISE:15\n")
            bot.evaluateOdds()
            move = bot.makeMove()
            print "SENDING A ", move, "ACTION TO ENGINE\n"
            s.send(move+'\n')
##            s.send("CHECK\n")
    # if we get here, the server disconnected us, so clean up the socket
    s.close()
