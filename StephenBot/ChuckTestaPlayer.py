import socket
import sys

from Player import Player
from ChuckTestaStrat import *
from FoldBotStrat import *

class ChuckTestaPlayer(Player):
    def __init__(self, port):
        Player.__init__(self, port)
        self.winningStrat = ChuckTestaStrat()
        self.losingStrat = self.winningStrat


if __name__ == "__main__":
    # port number specified by the engine to connect to.
    port = int(sys.argv[1])
    p = ChuckTestaPlayer(port)
    p.run()
