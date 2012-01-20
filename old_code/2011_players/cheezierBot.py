from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from pokerbots.player.LukeBot import LukeBot
from pokerbots.player.ourbot import *
from random import randint

class CheezierBot(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "CheezierBot"
        self.bot = cheezierbot()

class cheezierbot(LukeBot):
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        LukeBot.__init__(self)
        # my name
        self.name = "cheezierbot"
        ##Eq ranges for each street
        self.eq_ranges = {PREFLOP:[2, 40, 56, 85], FLOP:[2, 45, 65, 80],TURN:[2, 45, 65, 85],RIVER:[2, 45, 65, 85]}

    def preflop(self, brain):
        #it's preflop, tell me how to play
        if self.eq == 0: ##0
            self.fir = Call()
            self.che = Check()           
        elif self.eq == 1: ##30
            self.fir = Call()
            self.che = Check() 
        elif self.eq == 2: ##50
            self.fir = Call()
            self.che = Check()
            self.chebet = [[Call(), self.myallin], [Call(), self.myallin], [Fold()]]
            self.dealbet = [[Call(), self.myallin], [Call(), self.myallin], [Fold()]] 
        elif self.eq == 3: ##70
            self.fir = Raise(self.min + brain.pot)
            self.che = Raise(self.min + brain.pot)
            self.chebet = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Fold()]]
            self.dealbet = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Fold()]]
            self.betrairai = [[Fold(), self.myallin], [Fold(), self.myallin], [Fold()]] 
        elif self.eq == 4: ##85
            self.fir = Raise(self.min + brain.pot)
            self.che = Raise(self.min + brain.pot)
            self.chebet = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Call()]]
            self.dealbet = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Call()]]
            self.betrairai = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Call()]]
        else:
            print "flop: umm...", self.eq, brain.ev

###########Strategy to Take On Flop###################
    def flop(self, brain):
        #it's the flop, tell me how to play
        if self.eq == 0: ##0
            self.fir = Call()
            self.che = Check()           
        elif self.eq == 1: ##30
            self.fir = Call()
            self.che = Check() 
        elif self.eq == 2: ##50
            self.fir = Call()
            self.che = Check()
            self.chebet = [[Call(), self.myallin], [Call(), self.myallin], [Fold()]]
            self.dealbet = [[Call(), self.myallin], [Call(), self.myallin], [Fold()]]  
        elif self.eq == 3: ##70
            self.fir = Raise(self.min + brain.pot)
            self.che = Raise(self.min + brain.pot)
            self.chebet = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Fold()]]
            self.dealbet = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Fold()]]
            self.betrairai = [[Fold(), self.myallin], [Fold(), self.myallin], [Fold()]]  
        elif self.eq == 4: ##85
            self.fir = Raise(self.min + brain.pot)
            self.che = Raise(self.min + brain.pot)
            self.chebet = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Call()]]
            self.dealbet = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Call()]]
            self.betrairai = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Call()]]
        else:
            print "flop: umm...", self.eq, brain.ev

#############Action to Take on Turn###################
    def turn(self, brain):
        #it's the turn, tell me how to play
        if self.eq == 0: ##0
            self.fir = Call()
            self.che = Check()           
        elif self.eq == 1: ##30
            self.fir = Call()
            self.che = Check() 
        elif self.eq == 2: ##50
            self.fir = Call()
            self.che = Check()
            self.chebet = [[Call(), self.myallin], [Call(), self.myallin], [Fold()]]
            self.dealbet = [[Call(), self.myallin], [Call(), self.myallin], [Fold()]]  
        elif self.eq == 3: ##70
            self.fir = Raise(self.min + brain.pot)
            self.che = Raise(self.min + brain.pot)
            self.chebet = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Fold()]]
            self.dealbet = [[self.randaction(Raise(self.min + brain.pot), Call(), 95), self.myallin], [Call(), self.myallin], [Fold()]]
            self.betrairai = [[Fold(), self.myallin], [Fold(), self.myallin], [Fold()]]  
        elif self.eq == 4: ##85
            self.fir = Raise(self.min + brain.pot)
            self.che = Raise(self.min + brain.pot)
            self.chebet = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Call()]]
            self.dealbet = [[self.randaction(Raise(self.min + brain.pot), Call(), 95), self.myallin], [Call(), self.myallin], [Call()]]
            self.betrairai = [[self.randaction(Raise(self.min + brain.pot), Call(), 95), self.myallin], [Call(), self.myallin], [Call()]]
        else:
            print "turn: umm...", self.eq, brain.ev

    def river(self, brain):
        #it's the river, tell me how to play
        if self.eq == 0: ##0
            self.fir = Call()
            self.che = Check()           
        elif self.eq == 1: ##30
            self.fir = Call()
            self.che = Check() 
        elif self.eq == 2: ##50
            self.fir = Call()
            self.che = Check()
            self.chebet = [[Call(), self.myallin], [Call(), self.myallin], [Fold()]]
            self.dealbet = [[Call(), self.myallin], [Call(), self.myallin], [Fold()]]  
        elif self.eq == 3: ##70
            self.fir = Raise(self.min + brain.pot)
            self.che = Raise(self.min + brain.pot)
            self.chebet = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Fold()]]
            self.dealbet = [[self.randaction(Raise(self.min + brain.pot), Call(), 95), self.myallin], [Call(), self.myallin], [Fold()]]
            self.betrairai = [[Fold(), self.myallin], [Fold(), self.myallin], [Fold()]]  
        elif self.eq == 4: ##85
            self.fir = Raise(self.min + brain.pot)
            self.che = Raise(self.min + brain.pot)
            self.chebet = [[Raise(self.min + brain.pot), self.myallin], [Call(), self.myallin], [Call()]]
            self.dealbet = [[self.randaction(Raise(self.min + brain.pot), Call(), 95), self.myallin], [Call(), self.myallin], [Call()]]
            self.betrairai = [[self.randaction(Raise(self.min + brain.pot), Call(), 95), self.myallin], [Call(), self.myallin], [Call()]]
        else:
            print "river: umm...", self.eq, brain.ev
