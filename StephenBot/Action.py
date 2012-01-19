class Action:
    def __init__(self, type=None, player=None, potAmt=0, betAmt=0, amt=0,
                 handStrength=0):
        self.player = player 
        self.type = type
        self.potAmount = potAmt
        self.betAmount = betAmt
        self.amount = amt
        self.handStrength = handStrength

    def copy(self):
        return Action(self.type,
                      self.player,
                      self.potAmount,
                      self.betAmount,
                      self.amount,
                      self.handStrength)
    
