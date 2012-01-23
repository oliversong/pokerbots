class Card:
    def __init__(self, c):
        self.stringValue = c
        self.value = self.cardValue(c[0])
        self.suit = self.suitValue(c[1])

    def cardValue(self, v):
        if ord(v) in range(50, 58):  #values 2-9
            return int(v)
        elif v=='T' or v=='t':   #Ten
            return 10
        elif v=='J' or v=='j':   #Jack
            return 11
        elif v=='Q' or v=='q':   #QUeen
            return 12
        elif v=='K' or v=='k':   #King
            return 13
        elif v=='A' or v=='a':   #Ace
            return 14
        else:
            return -1    #default send nothing

    def suitValue(self, s):
        if s=='c' or s=='C':
            return 0
        elif s=='d' or s=='D':
            return 1
        elif s=='h' or s=='h':
            return 2
        elif s=='s' or s=='S':
            return 3
        else:
            return -1
