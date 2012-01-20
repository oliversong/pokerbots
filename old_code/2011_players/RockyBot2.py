from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from pokerbots.player.LukeBot import LukeBot
from pokerbots.player.ourbot import *
from random import randint

class RockyBot2(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "RockyBot2"
        self.bot = rockybot2()

class RockyBot3(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "RockyBot3"
        self.bot = rockybot2()
        self.bot.eq_ranges = [[5, 50, 85, 90], [45, 60, 65, 80], [5, 10, 65, 80], [10, 55, 75, 100]]

class RockyBot4(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "RockyBot4"
        self.bot = rockybot2()
        self.bot.eq_ranges = [[15, 40, 60, 90], [45, 55, 80, 80], [10, 15, 45, 90], [5, 35, 35, 70]]

class rockybot2(LukeBot):
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        LukeBot.__init__(self)
        # my name
        self.name = "rockybot2"
        ##Eq ranges for each street
        self.eq_ranges = {PREFLOP:[20, 40, 60, 87],FLOP:[20, 40, 60, 80],TURN:[20, 40, 60, 85],RIVER:[20, 40, 80, 90]}

    def preflop(self, brain):
        #it's preflop, tell me how to play
        if self.eq == 0: ##0
            self.fir = Fold()
            self.che = Check()
        elif self.eq == 1: ##20
            self.fir = Fold()
            self.che = Check()
        elif self.eq == 2: ##40
            self.fir = Fold()
            self.che = Check()
        elif self.eq == 3: ##60
            self.fir = Fold()
            self.che = Check()  
        elif self.eq == 4: ##87
            self.fir = Raise(self.myallin)
            self.che = Raise(self.myallin)
            self.dealbet = [[Raise(self.myallin), self.myallin], [Call(), self.oppallin], [Call()]]
        else:
            print "flop: umm...", eq, brain.ev

###########Strategy to Take On Flop###################
    def flop(self, brain):
        #it's the flop, tell me how to play
        if self.eq == 0: ##20
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1: ##40
            self.fir = self.randaction(Check(),Bet(brain.bb*3),50)
            self.che = Check()    
            self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), max(brain.pot/2,brain.bb*2)], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), max(brain.pot/2,brain.bb*2)], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]                 
        elif self.eq == 2: ##60
            self.fir = self.randaction(Check(),Bet(brain.bb*3),50)
            self.che = Check()    
            self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Raise(self.min), max(brain.pot/2,brain.bb*2)], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Raise(self.min), max(brain.pot/2,brain.bb*2)], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]
            self.betrairai = [[Fold(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
        elif self.eq == 3: ##80
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min), max(brain.pot/2,brain.bb*3)], [Call(), brain.pot], [Fold()]]
            self.dealbet = [[Raise(self.min), max(brain.pot/2,brain.bb*3)], [Call(), brain.pot], [Fold()]]            
            self.betrai = [[Call(), max(brain.pot,brain.bb*4)], [Fold(), self.oppallin], [Fold()]] 
            self.chebetrai = [[Call(), self.valuebet], [Fold, self.oppallin], [Fold()]] 
            self.betrairai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]                   
        elif self.eq == 4:
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min*2), brain.pot], [Raise(self.min), self.oppallin/2], [Call()]]
            self.dealbet = [[Raise(self.min*2), brain.pot], [Raise(self.min), self.oppallin/2], [Call()]]            
            self.betrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]] 
            self.chebetrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]] 
            self.betrairai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]      
        else:
            print "flop: umm...", eq, brain.ev

#############Action to Take on Turn###################
    def turn(self, brain):
        #it's the turn, tell me how to play
        if self.eq == 0: ##20
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1: ##40
            self.fir = self.randaction(Check(),Bet(brain.bb*3),50)
            self.che = Check()    
            self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), max(brain.pot/2,brain.bb*2)], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), max(brain.pot/2,brain.bb*2)], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]                 
        elif self.eq == 2: ##60
            self.fir = self.randaction(Check(),Bet(brain.bb*3),50)
            self.che = Check()    
            self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Raise(self.min), max(brain.pot/2,brain.bb*2)], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Raise(self.min), max(brain.pot/2,brain.bb*2)], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]
            self.betrairai = [[Fold(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
        elif self.eq == 3: ##85
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min), max(brain.pot/2,brain.bb*3)], [Call(), brain.pot], [Fold()]]
            self.dealbet = [[Raise(self.min), max(brain.pot/2,brain.bb*3)], [Call(), brain.pot], [Fold()]]            
            self.betrai = [[Call(), max(brain.pot,brain.bb*4)], [Fold(), self.oppallin], [Fold()]] 
            self.chebetrai = [[Call(), self.valuebet], [Fold, self.oppallin], [Fold()]] 
            self.betrairai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]                   
        elif self.eq == 4:
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min*2), brain.pot], [Raise(self.min), self.oppallin/2], [Call()]]
            self.dealbet = [[Raise(self.min*2), brain.pot], [Raise(self.min), self.oppallin/2], [Call()]]            
            self.betrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]] 
            self.chebetrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]] 
            self.betrairai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]      
        else:
            print "turn: umm...", eq, brain.ev

    def river(self, brain):
        #it's the river, tell me how to play
        if self.eq == 0: ##20
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1: ##40
            self.fir = self.randaction(Check(),Bet(brain.bb*3),50)
            self.che = Check()    
            self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), max(brain.pot/2,brain.bb*2)], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), max(brain.pot/2,brain.bb*2)], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]                 
        elif self.eq == 2: ##60
            self.fir = self.randaction(Check(),Bet(brain.bb*3),50)
            self.che = Check()    
            self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Fold(), max(brain.pot/2,brain.bb*2)], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Fold(), max(brain.pot/2,brain.bb*2)], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]
            self.betrairai = [[Fold(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
        elif self.eq == 3: ##80
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.valuebet),self.valuebet/2], [Call(), max(self.valuebet,brain.bb*3)], [Fold()]]
            self.dealbet = [[Raise(self.valuebet),self.valuebet/2], [Call(), max(self.valuebet,brain.bb*3)], [Fold()]]           
            self.betrai = [[Call(), max(self.valuebet,brain.bb*3)], [Fold(), self.oppallin], [Fold()]] 
            self.chebetrai = [[Call(), max(self.valuebet,brain.bb*3)], [Fold, self.oppallin], [Fold()]] 
            self.betrairai = [[Call(), max(self.valuebet,brain.bb*3)], [Fold(), self.oppallin], [Fold()]]                   
        elif self.eq == 4: ##90
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min*2), brain.pot], [Raise(self.min), self.oppallin/2], [Call()]]
            self.dealbet = [[Raise(self.min*2), brain.pot], [Raise(self.min), self.oppallin/2], [Call()]]            
            self.betrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]] 
            self.chebetrai = [[Raise(self.min), self.oppallin], [Call(), self.oppallin], [Call()]] 
            self.betrairai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]      
        else:
            print "river: umm...", eq, brain.ev
