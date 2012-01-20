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
                      self.potAmount,
                      self.betAmount,
                      self.amount,
                      self.handStrength)
    
