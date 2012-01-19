class Bot:
    pair = 0
    suited = 0
    faces = 0
    consecutive = 0
    oneFace = 0

    def __init__(self):
        self.holeCard1 = None
        self.holeCard2 = None
        self.state = None
        self.strategy = None

    def evaluateHandQualities(self):
        """
        if self.holeCard1.value == self.holeCard2.value:
            pair = 1
        if self.holeCard1.suit == self.holeCard2.suit:
            suited = 1
        if self.holeCard1.value>10 and self.holeCard2.value>10:
            faces = 1
        if self.holeCard1.value>10 or self.holeCard2.value>10:
            oneFace = 1
        if abs(self.holeCard1.value - self.holeCard2.value) == 1:
            consecutive = 1
        """

    def updateState(self, s):
        self.state = s

    def evaluateOdds(self):
        return self.strategy.evaluateOdds(self)
    def makeMove(self):
        return self.strategy.getMove(self)

    def isValidMove(self, move):
        return false

    def setHoleCards(self, c1, c2):
        self.holeCard1 = c1
        self.holeCard2 = c2
       # self.evaluateHandQualities()

