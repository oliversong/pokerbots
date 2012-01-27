from Strategy import *
from Enums import *
from Move import *

class CallRaiseStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def getMove(self, game, archive):

        if game.street==RIVER:
            return self.pushMin(game)

        return Move(CALL)
