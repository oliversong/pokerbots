from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from pokerbots.player.LukeBot import LukeBotNew
from pokerbots.player.ourbot import *
from random import randint

class FlyingSpagBot(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "FlyingSpagBot"
        self.bot = flyingspagbot()

class flyingspagbot(LukeBotNew):
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        LukeBotNew.__init__(self)
        # my name
        self.name = "flyingspagbot"
        ##Eq ranges for each street
        self.eq_ranges = {PREFLOP:[50, 70],FLOP:[60, 80],TURN:[65, 85],RIVER:[75, 90]}

    def preflop(self, brain):
        #it's preflop, tell me how to play
        if self.eq == 0: ##0
            self.fir = Call()
            self.che = Check()
        elif self.eq == 1: ##80
            self.fir = Raise(max(16,self.min))
            self.che = Raise(max(16,self.min))
            self.chebet = [[Call(), 32], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Call(), 32], [Fold(), self.oppallin], [Fold()]]                
            self.betrai = [[Call(), 64], [Fold(), self.oppallin], [Fold()]]
            self.betrairai = [[Call(), 64], [Fold(), self.oppallin], [Fold()]]            
        elif self.eq == 2: ##90
            self.fir = Raise(max(16,self.min))
            self.che = Raise(max(16,self.min))
            self.chebet = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]
            self.dealbet = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]            
            self.betrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Fold()]]
            self.betrairai = [[Call(), self.oppallin], [Call(), self.oppallin], [Fold()]]            
        else:
            print "flop: umm...", self.eq, brain.ev

###########Strategy to Take On Flop###################
    def flop(self, brain):
        #it's the flop, tell me how to play
        if self.eq == 0: ##0
            self.fir = Check()
            self.che = Check()                              
        elif self.eq == 1: ##80
            self.fir = Check()
            self.che = Check()
            self.chebet = [[Call(), max(brain.pot/2,80)], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Call(), max(brain.pot/2,80)], [Fold(), self.oppallin], [Fold()]]                           
        elif self.eq == 2: ##90
            self.fir = Check()
            self.che = Check()
            self.chebet = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]
            self.dealbet = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]             
        else:
            print "flop: umm...", self.eq, brain.ev

#############Action to Take on Turn###################
    def turn(self, brain):
        #it's the turn, tell me how to play
        if self.eq == 0: ##0
            self.fir = Check()
            self.che = Check()                              
        elif self.eq == 1: ##80
            self.fir = Check()
            self.che = Check()
            self.chebet = [[Call(), max(brain.pot/2,80)], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Call(), max(brain.pot/2,80)], [Fold(), self.oppallin], [Fold()]]                     
        elif self.eq == 2: ##90
            self.fir = Check()
            self.che = Check()
            self.chebet = [[Raise(self.min), self.myallin/2], [Raise(self.myallin), self.myallin], [Call()]]
            self.dealbet = [[Raise(self.min), self.myallin/2], [Raise(self.myallin), self.myallin], [Call()]]          
            self.betrai = [[Raise(self.min), self.myallin/2], [Raise(self.myallin), self.myallin], [Call()]]  
            self.betrairai = [[Raise(self.min), self.myallin/2], [Raise(self.myallin), self.myallin], [Call()]]    
        else:
            print "turn: umm...", self.eq, brain.ev


    def river(self, brain):
        #it's the river, tell me how to play
        if self.eq == 0: ##0
            self.fir = Check()
            self.che = Check()                              
        elif self.eq == 1: ##80
            self.fir = Check()
            self.che = Check()
            self.chebet = [[Call(), max(brain.pot/2,150)], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Call(), max(brain.pot/2,150)], [Fold(), self.oppallin], [Fold()]]                   
        elif self.eq == 2: ##95
            self.fir = Bet(brain.pot*2)
            self.che = Bet(brain.pot*2)
            self.chebet = [[Raise(self.min), self.myallin/2], [Raise(self.myallin), self.myallin], [Call()]]
            self.dealbet = [[Raise(self.min), self.myallin/2], [Raise(self.myallin), self.myallin], [Call()]]          
            self.betrai = [[Raise(self.min), self.myallin/2], [Raise(self.myallin), self.myallin], [Call()]]
            self.chebetrai = [[Raise(self.min), self.myallin/2], [Raise(self.myallin), self.myallin], [Call()]]          
            self.betrairai = [[Raise(self.min), self.myallin/2], [Raise(self.myallin), self.myallin], [Call()]]   
        else:
            print "river: umm...", self.eq, brain.ev
