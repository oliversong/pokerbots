import matplotlib.pyplot as plt

class PlotBankrolls():

    def __init__(self):
        self.myBank = []
        self.leftBank = []
        self.rightBank = []
        self.leftOpp = ""
        self.rightOpp = ""

    def addMoreBanks(self, myB, lB, rB):
        self.myBank += [myB]
        self.leftBank += [lB]
        self.rightBank += [rB]

    def plotBanks(self):
        t = [i for i in range(len(self.myBank))]
        plt.plot(t, self.myBank, 'r--', t, self.leftBank, 'bs', t, self.rightBank, 'g^')
        plt.legend(("My bankroll", self.leftOpp, self.rightOpp), loc='upper left')
        plt.savefig("chucktestaplot.png")
