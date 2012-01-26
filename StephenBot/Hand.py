from Enums import *

class Hand:
    def __init__(self):
        self.actions = None
        self.splitActions = None
        self.trackedActions = [CHECK, BET, RAISE, CALL, POST]
        self.clearHand()

    def clearHand(self):
        self.actions = []
        self.splitActions = [[],[],[],[]]

    def printHand(self):
        print "PRINTING HAND"
        for street in self.splitActions:
            print "STREET"
            for a in street:
                if a.amount:
                    print "[", a.type, ",", a.player, ",", a.amount, "]"
                else:
                    print "[", a.type, ",", a.player, "]"

    def splitActionsList(self):
        s = 0
        self.splitActions = [[],[],[],[]]
        for a in self.actions:
            if a.type == DEAL:
                s += 1
            if a.type in self.trackedActions:
                self.splitActions[s].append(a)

    def recentOppMove(self):
        if self.actions[-1].type in [DEAL, POST]:
            return []
        elif self.actions[-2].type in [DEAL, POST]:
            return [self.actions[-1]]
        else:
            return[self.actions[-1], self.actions[-2]]
