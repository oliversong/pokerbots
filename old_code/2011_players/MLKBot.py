from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from pokerbots.player.LukeBot import LukeBot
from pokerbots.player.ourbot import *
from random import randint

class MLKBot(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "MLKBot"
        self.bot = mlkbot()

class mlkbot(LukeBot):
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        LukeBot.__init__(self)
        # my name
        self.name = "mlkbot"
        ##Eq ranges for each street
        self.eq_ranges = {PREFLOP:[50, 70, 80, 90],FLOP:[50, 70, 80, 90],TURN:[50, 75, 85, 92],RIVER:[50, 80, 90, 95]}

#    def respond(self, brain):
#        return LukeBot.respond(self,brain)

    def preflop(self, brain):
        #it's preflop, tell me how to play
        my_action = None
        if self.eq == 0: ##0
            self.fir = Call()
            self.che = Check()
        elif self.eq == 1: ##50
            self.fir = Call()
            self.che = Check()
            self.chebet = [[Call(), brain.bb*3], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Call(), 10], [Fold(), self.oppallin], [Fold]]
            self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold]]
        elif self.eq == 2: ##70
            self.fir = Call()
            self.che = Check()
            self.chebet = [[Call(), brain.bb*7], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Call(), brain.bb*7], [Fold(), self.oppallin], [Fold]]
            self.betrairai = [[Call(), 12], [Fold(), self.oppallin], [Fold]]  
        elif self.eq == 3: ##80
            self.fir = Raise(brain.bb*3)
            self.che = Raise(brain.bb*3)
            self.chebet = [[Raise(self.min), brain.bb*3], [Call(), brain.bb*6], [Fold()]]
            self.dealbet = [[Raise(self.min), brain.bb*3], [Call(), brain.bb*6], [Fold()]]      
            self.betrairai = [[Call(), brain.bb*6], [Fold(), self.oppallin], [Fold]]    
        elif self.eq == 4: ##90
            self.fir = Raise(brain.bb*5)
            self.che = Raise(brain.bb*5)
            self.chebet = [[Raise(brain.bb*8), brain.bb*4], [Raise(self.min), brain.bb*12], [Call()]]
            self.dealbet = [[Raise(brain.bb*8), brain.bb*4], [Raise(self.min), brain.bb*12], [Call()]]
            self.betrairai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]
        else:
            print "flop: umm...", self.eq, brain.ev

###########Strategy to Take On Flop###################
    def flop(self, brain):
        #it's the flop, tell me how to play
        my_action = None
        if self.eq == 0: ##0
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1: ##50
            self.fir = Bet(brain.pot/2)
            self.che = Check()    
            self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), brain.bb*2], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), brain.bb*2], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]                 
        elif self.eq == 2: ##70
            self.fir = Bet(brain.bb*4)
            self.che = Bet(brain.bb*4)    
            self.betrai = [[Call(), brain.bb*13], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), brain.bb*13], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), brain.bb*13], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Call(), brain.bb*13], [Fold(), self.oppallin], [Fold()]]
            self.betrairai = [[Call(), brain.bb*13], [Fold(), self.oppallin], [Fold()]]
        elif self.eq == 3: ##80
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min), self.valuebet], [Call(), brain.pot], [Fold()]]
            self.dealbet = [[Raise(self.min), self.valuebet], [Call(), brain.pot], [Fold()]]          
            self.betrai = [[Call(), self.myallin/2], [Fold(), self.oppallin], [Fold()]] 
            self.chebetrai = [[Call(), self.myallin/3], [Fold, self.oppallin], [Fold()]] 
            self.betrairai = [[Call(), self.myallin/3], [Fold(), self.oppallin], [Fold()]]                   
        elif self.eq == 4: ##90
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min), self.valuebet*2], [Call(), self.oppallin], [Call()]]
            self.dealbet = [[Raise(self.min), self.valuebet*2], [Call(), self.oppallin], [Call()]]          
            self.betrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]] 
            self.chebetrai = [[Call(), self.myallin/3], [Call(), self.oppallin], [Call()]] 
            self.betrairai = [[Call(), self.myallin/3], [Call(), self.oppallin], [Call()]]    
        else:
            print "flop: umm...", self.eq, brain.ev

#############Action to Take on Turn###################
    def turn(self, brain):
        #it's the turn, tell me how to play
        my_action = None
        if self.eq == 0: ##0
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1: ##50
            self.fir = Bet(brain.pot/2)
            self.che = Check()    
            self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), brain.bb*2], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), brain.bb*2], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]                 
        elif self.eq == 2: ##70
            self.fir = Bet(brain.bb*4)
            self.che = Bet(brain.bb*4)    
            self.betrai = [[Call(), brain.bb*13], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), brain.bb*13], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), brain.bb*13], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Call(), brain.bb*13], [Fold(), self.oppallin], [Fold()]]
            self.betrairai = [[Call(), brain.bb*13], [Fold(), self.oppallin], [Fold()]]
        elif self.eq == 3: ##80
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min), self.valuebet], [Call(), brain.pot], [Fold()]]
            self.dealbet = [[Raise(self.min), self.valuebet], [Call(), brain.pot], [Fold()]]          
            self.betrai = [[Call(), self.myallin/2], [Fold(), self.oppallin], [Fold()]] 
            self.chebetrai = [[Call(), self.myallin/3], [Fold, self.oppallin], [Fold()]] 
            self.betrairai = [[Call(), self.myallin/3], [Fold(), self.oppallin], [Fold()]]                   
        elif self.eq == 4: ##90
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min), self.valuebet*2], [Call(), self.oppallin], [Call()]]
            self.dealbet = [[Raise(self.min), self.myallin/3], [Raise(self.myallin), self.myallin], [Call()]]          
            self.betrai = [[Raise(self.min*2), self.myallin/3], [Raise(self.myallin), self.myallin], [Call()]] 
            self.chebetrai = [[Raise(self.min*2), self.myallin/3], [Raise(self.myallin), self.myallin], [Call()]] 
            self.betrairai = [[Raise(self.myallin), self.myallin], [Call(), self.oppallin], [Call()]]    
        else:
            print "turn: umm...", self.eq, brain.ev


    def river(self, brain):
        #it's the river, tell me how to play
        my_action = None
        if self.eq == 0: ##0
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1: ##50
            self.fir = Bet(brain.pot/2)
            self.che = Check()    
            self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), brain.bb*2], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), brain.bb*2], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]                 
        elif self.eq == 2: ##80
            self.fir = Bet(brain.bb*8)
            self.che = Bet(brain.bb*8)    
            self.betrai = [[Call(), brain.bb*25], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), brain.bb*25], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), brain.bb*25], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Call(), brain.bb*25], [Fold(), self.oppallin], [Fold()]]
            self.betrairai = [[Call(), brain.bb*25], [Fold(), self.oppallin], [Fold()]]
        elif self.eq == 3: ##90
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min), self.valuebet], [Call(), brain.pot], [Call()]]
            self.dealbet = [[Raise(self.min), self.valuebet], [Call(), brain.pot], [Call()]]          
            self.betrai = [[Call(), self.myallin/2], [Call(), self.oppallin], [Call()]] 
            self.chebetrai = [[Call(), self.myallin/3], [Call, self.oppallin], [Call()]] 
            self.betrairai = [[Call(), self.myallin/3], [Call(), self.oppallin], [Call()]]                   
        elif self.eq == 4: ##95
            self.fir = Bet(self.myallin)
            self.che = Bet(self.myallin)
            self.chebet = [[Raise(self.myallin), self.myallin], [Call(), self.oppallin], [Call()]]
            self.dealbet = [[Raise(self.myallin), self.myallin], [[Call(), self.oppallin], [Call()]]]         
            self.betrai = [[Raise(self.myallin), self.myallin], [Call(), self.oppallin], [Call()]]
            self.chebetrai = [[Raise(self.myallin), self.myallin], [Call(), self.oppallin], [Call()]] 
            self.betrairai = [[Raise(self.myallin), self.myallin], [Call(), self.oppallin], [Call()]]   
        else:
            print "river: umm...", self.eq, brain.ev
