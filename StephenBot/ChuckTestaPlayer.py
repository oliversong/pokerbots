import socket
import sys

from Player import Player
from ChuckTestaStrat import *
from FoldBotStrat import *

if __name__ == "__main__":
    # port number specified by the engine to connect to.
    port = int(sys.argv[1])
    p = Player(port)
    p.winningStrat = ChuckTestaStrat()
    p.losingStrat = FoldBotStrategy()
    p.run()
