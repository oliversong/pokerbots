import socket
import sys

from Player import Player
from CallRaiseStrategy import *

if __name__ == "__main__":
    # port number specified by the engine to connect to.
    port = int(sys.argv[1])
    p = Player(port)
    p.strategy = CallRaiseStrategy()
    p.run()
