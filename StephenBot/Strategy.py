from pokereval import PokerEval

class Strategy:
    def __init__(self):
        self.pokereval = PokerEval()
        self.handRank = None

    def evaluateOdds(self, b):
        raise NotImplementedError("evaluateOdds not implemented in subclass")
    def getMove(self, b):
        raise NotImplementedError("getMove not implemented in subclass")
    

