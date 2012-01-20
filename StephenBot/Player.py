import socket
import sys

from Bot import *
from GameState import *
from LooseAgressiveStrategy import *


"""
Simple example pokerbot, written in python. This is an example of a bare bones,
dumb pokerbot - it only sets up the socket necessary to connect with the engine
and then always returns the same action. It is meant as an example of how a
pokerbot should communicate with the engine.
"""

if __name__ == "__main__":
    # port number specified by the engine to connect to.
    port = int(sys.argv[1])
    # initialize a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect the socket to the engine
    s.connect(('localhost', port))
    fs = s.makefile()

    bot = Bot()
    game = GameState()
    lag = LooseAgressiveStrategy()
    
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
#        print "THIS IS A NEW PACKET"
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
            bot.strategy = lag

        if game.state == "GETACTION":
##            s.send("RAISE:15\n")
            bot.evaluateOdds()
            move = bot.makeMove()
            print "SENDING A ", move, "ACTION TO ENGINE\n"
            s.send(move+'\n')
##            s.send("CHECK\n")
    # if we get here, the server disconnected us, so clean up the socket
    s.close()
