import socket
import sys

from Player import Player
from FoldBotStrat import *

if __name__ == "__main__":
    # port number specified by the engine to connect to.
    port = int(sys.argv[1])
    p = Player(port)
    p.strategy = FoldBotStrategy()
    p.winningStrat = FoldBotStrategy()
    p.losingStrat = FoldBotStrategy()
    p.run()
