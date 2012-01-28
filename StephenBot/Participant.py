from Card import *

class Participant():
    def __init__(self, name=""):
        self.name = name
        self.bankroll = 0
        self.newHand()

    def newHand(self):
        self.position = None
        self.stack = 200
        self.active = 1
        self.pip = 0

        self.holeCard1 = None
        self.holeCard2 = None
        self.lastActions = []
