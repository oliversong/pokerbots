from Enums import *

class Hand:
    def __init__(self):
        self.actions = None
        self.splitActions = None
        self.trackedActions = [CHECK, BET, RAISE, CALL]
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
        for a in self.actions:
#            print "SPLIT ACTIONS LIST TYPE"
#            print a.type
            if a.type == DEAL:
                s += 1
            if a.type in self.trackedActions:
                self.splitActions[s].append(a)

