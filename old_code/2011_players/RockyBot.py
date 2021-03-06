from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from pokerbots.player.LukeBot import LukeBot
from pokerbots.player.ourbot import *
from random import randint

class RockyBot(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "RockyBot"
        self.bot = rockybot()
        
class rockybot(LukeBot):
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        LukeBot.__init__(self)
        # my name
        self.name = "rockybot"
        ##Eq ranges for each street
        self.eq_ranges = {PREFLOP:[20, 40, 60, 90],FLOP:[20, 40, 60, 80],TURN:[20, 40, 60, 85],RIVER:[20, 40, 80, 90]}

    def preflop(self, brain):
        #it's preflop, tell me how to play
        my_action = None
        if self.eq == 0: ##20
            self.fir = Call()
            self.che = Check()
        elif self.eq == 1: ##40
            self.fir = Call()
            self.che = Raise(brain.bb*3)
            self.chebet = [[Fold(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Call(), self.min], [Fold(), self.oppallin], [Fold]]
            self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold]]
        elif self.eq == 2: ##60
            self.fir = Raise(brain.bb*3)
            self.che = Raise(brain.bb*3)
            self.chebet = [[Call(), brain.bb*2], [Call(), brain.bb*4], [Fold()]]
            self.dealbet = [[Raise(self.min), brain.bb*3], [Call(), brain.bb*6], [Fold]]
            self.betrairai = [[Call(), 12], [Fold(), self.oppallin], [Fold]]  
        elif self.eq == 3: ##90
            self.fir = Raise(brain.bb*3)
            self.che = Raise(brain.bb*3)
            self.chebet = [[Raise(self.min), brain.bb*3], [Call(), brain.bb*6], [Fold()]]
            self.dealbet = [[Raise(self.min), brain.bb*3], [Call(), brain.bb*6], [Fold()]]      
            self.betrairai = [[Call(), brain.bb*6], [Fold(), self.oppallin], [Fold]]    
        elif self.eq == 4: ##100
            self.fir = Raise(brain.bb*3)
            self.che = Raise(brain.bb*3)
            self.chebet = [[Raise(brain.bb*6), brain.bb*3], [Raise(self.min), brain.bb*6], [Call()]]
            self.dealbet = [[Raise(brain.bb*6), brain.bb*3], [Raise(self.min), brain.bb*6], [Call()]]
            self.betrairai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]
        else:
            print "flop: umm...", self.eq, brain.ev

###########Strategy to Take On Flop###################
    def flop(self, brain):
        #it's the flop, tell me how to play
        my_action = None
        if self.eq == 0: ##20
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1: ##40
            self.fir = self.randaction(Check(),Bet(brain.bb*3),50)
            self.che = Check()    
            self.betrai= [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
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
            print "flop: umm...", self.eq, brain.ev

#############Action to Take on Turn###################
    def turn(self, brain):
        #it's the turn, tell me how to play
        my_action = None
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
            print "turn: umm...", self.eq, brain.ev

    def river(self, brain):
        #it's the river, tell me how to play
        my_action = None
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
            print "river: umm...", self.eq, brain.ev
