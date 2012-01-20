from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from pokerbots.player.LukeBot import LukeBot
from pokerbots.player.ourbot import *
from random import randint

class MLKBot2(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "MLKBot2"
        self.bot = mlkbot2()

class MLKBot2Cool4U(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "MLKBot2Cool4U"
        self.bot = mlkbot2()
        self.bot.eq_ranges = [[30, 60, 85, 95], [20, 35, 45, 55], [15, 45, 45, 80], [5, 15, 35, 40]]

class MalcomXBot(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "MalcomXBot"
        self.bot = mlkbot2()
        self.bot.eq_ranges = [[20, 45, 50, 90], [5, 55, 70, 75], [10, 35, 75, 90], [5, 85, 90, 95]]

class MalcomXBot1(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "MalcomXBot1"
        self.bot = mlkbot2()
        self.bot.eq_ranges = [[15, 40, 45, 55], [5, 40, 55, 80], [40, 40, 65, 95], [5, 15, 95, 95]]

class MalcomXBot2(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        #good, but destroys manbearpig
        self.name = "MalcomXBot2"
        self.bot = mlkbot2()
        self.bot.eq_ranges = [[50, 55, 60, 70], [40, 45, 55, 55], [30, 45, 45, 100], [15, 30, 65, 90]]

class mlkbot2(LukeBot):
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        LukeBot.__init__(self)
        # my name
        self.name = "mlkbot2"
        ##Eq ranges for each street
        self.eq_ranges = {PREFLOP:[50, 60, 70, 80],FLOP:[50, 60, 70, 80],TURN:[50, 60, 70, 85],RIVER:[50, 60, 75, 85]}

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
            self.dealbet = [[Call(), 10], [Fold(), self.oppallin], [Fold()]]
            self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]
        elif self.eq == 2: ##70
            self.fir = Call()
            self.che = Check()
            self.chebet = [[Call(), brain.bb*7], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Call(), brain.bb*7], [Fold(), self.oppallin], [Fold()]]
            self.betrairai = [[Call(), 12], [Fold(), self.oppallin], [Fold()]]  
        elif self.eq == 3: ##80
            self.fir = Raise(brain.bb*3)
            self.che = Raise(brain.bb*3)
            self.chebet = [[Raise(self.min), brain.bb*3], [Call(), brain.bb*10], [Fold()]]
            self.dealbet = [[Raise(self.min), brain.bb*3], [Call(), brain.bb*10], [Fold()]]      
            self.betrairai = [[Call(), brain.bb*6], [Fold(), self.oppallin], [Fold()]]    
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
            self.chebet = [[Raise(self.min), self.valuebet], [Call(), brain.pot*2], [Fold()]]
            self.dealbet = [[Raise(self.min), self.valuebet], [Call(), brain.pot*2], [Fold()]]          
            self.betrai = [[Call(), self.myallin/2], [Fold(), self.oppallin], [Fold()]] 
            self.chebetrai = [[Call(), self.myallin/3], [Fold(), self.oppallin], [Fold()]] 
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
            self.chebetrai = [[Call(), self.myallin/3], [Fold(), self.oppallin], [Fold()]] 
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
            self.chebetrai = [[Call(), self.myallin/3], [Call(), self.oppallin], [Call()]] 
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
