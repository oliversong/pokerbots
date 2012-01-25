from Enums import *

class Action:
    def __init__(self, type, player, c1, c2, potAmt=0, betAmt=0, amt=0,
                 handStrength=0):
        self.player = player
        self.type = type
        self.potAmount = potAmt
        self.betAmount = betAmt
        self.amount = amt
        self.handStrength = handStrength

        self.showCard1 = c1
        self.showCard2 = c2

    def copy(self):
        return Action(self.type,
                      self.player,
                      self.showCard1,
                      self.showCard2,
                      self.potAmount,
                      self.betAmount,
                      self.amount,
                      self.handStrength)

    def __repr__(self):
        return "%s %s [%3.f, %.3f, %.3f] %d" % (self.player, ACTION_TYPES[self.type],
                                          self.amount, self.betAmount,
                                          self.potAmount, self.handStrength)
