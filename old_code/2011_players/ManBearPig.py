from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from pokerbots.player.LukeBot import LukeBot
from pokerbots.player.ourbot import *
from random import randint

class ManBearPigBot(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "ManBearPigBot"
        self.bot = manbearpigbot()

class ManBearPigBot1(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "ManBearPigBot1"
        self.bot = manbearpigbot()
        self.bot.eq_ranges = [[25, 80, 85, 90], [30, 45, 65, 100], [45, 55, 70, 90], [20, 25, 45, 75]]
        

class ManBearPigBot2(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "ManBearPigBot2"
        self.bot = manbearpigbot()
        self.bot.eq_ranges = [[40, 70, 80, 85], [10, 30, 40, 100], [5, 40, 55, 60], [30, 35, 60, 70]]

class manbearpigbot(LukeBot):
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        LukeBot.__init__(self)
        # my name
        self.name = "manbearpigbot"
        ##Eq ranges for each street
        self.eq_ranges = {PREFLOP:[30, 50, 70, 85],FLOP:[30, 50, 70, 91],TURN:[30, 50, 70, 85],RIVER:[50, 70, 80, 95]}

    def preflop(self, brain):
        #it's preflop, tell me how to play
        
	if self.eq == 2:
            if (brain.stack/ 10)< 25:
            	self.fir = Raise(8)
            	self.che = Raise(8)
            	self.chebet = [[Call(), 20], [Call(), brain.stack/5], [Fold()]]
            	self.dealbet = [[Call(), brain.stack/ 10], [Fold(), 31], [Fold()]]
            	self.betrairai = [[Call(), 50], [Fold(), self.oppallin], [Fold()]]  

	if self.eq == 3: ##70
		if (brain.stack/ 5)< 31:
        		self.fir = Raise(brain.bb*4)
			self.che = Raise(brain.bb*4)
        		self.chebet = [[Fold(), brain.bb*3], [Call(), brain.bb*6], [Fold()]]
        		self.dealbet = [[Raise(self.min), 16], [Call(), brain.stack/5], [Fold()]]      
        		self.betrairai = [[Call(), 65], [Fold(), self.oppallin], [Fold()]]  

	if self.eq == 0: ##0
            self.fir = Call()
            self.che = Raise(8)
            self.chebet = [[Fold(), brain.bb*3], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Fold(), 10], [Fold(), 20], [Fold()]]
            self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]            
        elif self.eq == 1: ##30
            self.fir = Raise(8)
            self.che = Raise(8)
            self.chebet = [[Fold(), brain.bb*3], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Call(), 11], [Fold(), 20], [Fold()]]
            self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]
        elif self.eq == 2: ##50
            self.fir = Raise(8)
            self.che = Raise(8)
            self.chebet = [[Call(), 20], [Call(), brain.stack/5], [Fold()]]
            self.dealbet = [[Call(), 25], [Fold(), 31], [Fold()]]
            self.betrairai = [[Call(), 50], [Fold(), self.oppallin], [Fold()]]  
        elif self.eq == 3: ##70
            self.fir = Raise(brain.bb*4)
            self.che = Raise(brain.bb*4)
            self.chebet = [[Fold(), brain.bb*3], [Call(), brain.bb*6], [Fold()]]
            self.dealbet = [[Raise(self.min), 16], [Call(), 31], [Fold()]]      
            self.betrairai = [[Call(), 50], [Fold(), self.oppallin], [Fold()]]    
        elif self.eq == 4: ##85
            self.fir = Raise(brain.bb*4)
            self.che = Raise(brain.bb*4)
            self.chebet = [[Raise(brain.bb*8), brain.bb*4], [Raise(self.min), brain.bb*12], [Call()]]
            self.dealbet = [[Raise(self.min*2), 11], [Raise(self.min), self.myallin/15], [Call()]]
            self.betrairai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]
        else:
            print "flop: umm...", self.eq, brain.ev

###########Strategy to Take On Flop###################
    def flop(self, brain):
        #it's the flop, tell me how to play
        my_action = None
        comm= brain.board.flop()
        S=False
        #####Example#######
        ##          1st act   1st cuttoff   2nd act   2nd cutoff   3rd act for bets higher than 2nd cutoff
        ##self.betrai = [[Call(), self.valuebet], [Fold(),self.oppallin],[Fold()]]

        if self.eq == 1: ##30
            if randint(0,99)< 70:
                if brain.opp_stats['AF']< .5:
                    S = sum([i.rank==14 or i.rank==13 for i in comm]) + sum([i.rank==j.rank for i in comm for j in comm if i!=j and i.rank>=8]) > 0
            if S:
                self.fir = Check() 
                self.che = Bet(randint(20,25))    
                self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
                self.dealbet = [[Call(), 8], [Fold(), self.oppallin], [Fold()]]
                self.chebet = [[Call(), 8], [Fold(), self.oppallin], [Fold()]]                 
                self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]] 

        if self.eq==2:   ##50
            if randint(0,99)< 80:
                if brain.pot>= 16:
                    if brain.opp_stats['AF']< .6:
                       S = sum([i.rank>=12 for i in comm]) + sum([i.rank==j.rank for i in comm for j in comm if i!=j and i.rank>=8]) > 0
            if S:
                self.fir = Bet(randint(15,25))
                self.che = Bet(randint(20,32))   
                self.betrai = [[Fold(), 10], [Fold(),self.oppallin],[Fold()]]
                self.dealbet = [[Call(), 16], [Fold(), self.oppallin], [Fold()]]
                self.chebet = [[Call(), 6], [Fold(), self.oppallin], [Fold()]]                 
                self.chebetrai = [[self.randaction(Call(), Fold(), brain.opp_stats['CHBR']*100), 65], [Fold(), self.oppallin], [Fold()]]  



        if self.eq == 0: ##0
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1: ##30
            self.fir = Check()
            self.che = Check() 
            self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), randint(8,13)], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), randint(8,13)], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]
            if brain.opp_stats['AF']< .7:
                self.fir = Bet(randint(8,17))
                self.che = Bet(randint(8,17))
        elif self.eq == 2: ##50
            self.fir = Bet(randint(10,21))
            self.che = Bet(randint(10,21))
            self.betrai = [[Call(), 40], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[self.randaction(Call(),Fold(), 67), 40], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), brain.bb*10], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), brain.bb*13], [Fold(), self.oppallin], [Fold()]]
            if brain.opp_stats['CHBR']> .2:
                self.chebetrai = [[Call(), 27], [Fold(), 34], [Fold()]]
        elif self.eq == 3: ##70
            self.fir = Bet(randint(12,20)) 
            self.che = Bet(randint(12,20)) 
            self.chebet = [[Raise(self.min), self.valuebet], [Call(), brain.pot], [Fold()]]
            self.dealbet = [[Call(), min(40, brain.stack/10)], [Call(), brain.pot], [Fold()]]          
            self.betrai = [[Call(), randint(45,60)], [Fold(), self.oppallin], [Fold()]] 
            self.chebetrai = [[Fold(), self.myallin/3], [Fold, self.oppallin], [Fold()]] 
            self.betrairai = [[Call(), self.myallin/3], [Fold(), self.oppallin], [Fold()]]
            if brain.opp_stats['CHBR']> .2:
                self.chebetrai = [[Call(), 50], [Call(), 70], [Fold()]]
        elif self.eq == 4: ##91
            self.fir = Bet(randint(20,30)) 
            self.che = Bet(randint(20,30)) 
            self.chebet = [[Raise(self.min), self.valuebet*2], [Call(), self.oppallin], [Call()]]
            self.dealbet = [[Call(), 7], [Call(), self.oppallin], [Call()]]          
            self.betrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]] 
            self.chebetrai = [[Call(), self.myallin/2], [Fold(), self.oppallin], [Fold()]] 
            self.betrairai = [[Call(), self.myallin/2], [Fold(), self.oppallin], [Fold()]]
            if brain.opp_stats['AF']> 1.5:
                self.fir = Check()
                self.chebet = [[Call(), self.valuebet*2], [Call(), self.oppallin], [Call()]]
                self.dealbet = [[Call(), 40], [Call(), self.oppallin], [Call()]]
                self.chebetrai = [[Call(), self.myallin/2], [Call(), self.oppallin], [Call()]] 
                self.betrairai = [[Call(), self.myallin/2], [Call(), self.myallin*.75], [Fold()]]
        else:
            print "flop: umm...", self.eq, brain.ev

#############Action to Take on Turn###################
    def turn(self, brain):
        #it's the turn, tell me how to play
        my_action = None
        comm= brain.board.flop()+ (brain.board.turn(),)
        turn= brain.board.turn()
        S= False
        #####Example#######
        ##          1st act   1st cuttoff   2nd act   2nd cutoff   3rd act for bets higher than 2nd cutoff
        ##self.betrai = [[Call(), self.valuebet], [Fold(),self.oppallin],[Fold()]]

        if self.eq == 1: ##30
            if randint(0,99)< 70:
                if brain.opp_stats['AF']< .5:
                    S = sum([turn.rank==14 or turn.rank==13]) + sum([i.rank==j.rank for i in comm for j in comm if i!=j and i.rank>=8]) > 0
            if S:
                self.fir = Check() 
                self.che = Bet(randint(20,25))    
                self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
                self.dealbet = [[Call(), 8], [Fold(), self.oppallin], [Fold()]]
                self.chebet = [[Call(), 8], [Fold(), self.oppallin], [Fold()]]                 
                self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]] 

        if self.eq==2:   ##50
            if randint(0,99)< 80:
                if brain.pot>= 16:
                    if brain.opp_stats['AF']< .5:
                       S = sum([turn.rank>=12 for i in comm]) + sum([i.rank==j.rank for i in comm for j in comm if i!=j and i.rank>=8]) > 0
            if S:
                self.fir = Bet(randint(15,25))
                self.che = Bet(randint(20,32))   
                self.betrai = [[Fold(), 10], [Fold(),self.oppallin],[Fold()]]
                self.dealbet = [[Call(), 16], [Fold(), self.oppallin], [Fold()]]
                self.chebet = [[Call(), 6], [Fold(), self.oppallin], [Fold()]]                 
                self.chebetrai = [[self.randaction(Call(), Fold(), brain.opp_stats['CHBR']*100), 65], [Fold(), self.oppallin], [Fold()]]  


        if self.eq == 0: ##0
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1: ##30
            self.fir = Check()
            self.che = Check() 
            self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), randint(8,13)], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), randint(8,13)], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]
            if brain.opp_stats['AF']< .7:
                self.fir = self.randaction(Bet(randint(8,17)), Check(), 50)
                self.che = self.randaction(Bet(randint(8,17)), Check(), 50)           
        elif self.eq == 2: ##50
            self.fir = Bet(randint(10,21))
            self.che = Bet(randint(10,21))
            self.betrai = [[Call(), 40], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), 20], [self.randaction(Call(),Fold(), 50), 30], [Fold()]]
            self.chebet = [[Call(), brain.bb*10], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), brain.bb*13], [Fold(), self.oppallin], [Fold()]]
            if brain.opp_stats['CHBR']> .2:
                self.chebetrai = [[Call(), 27], [Fold(), 34], [Fold()]]
        elif self.eq == 3: ##70
            self.fir = Bet(randint(12,20)) 
            self.che = Bet(randint(12,20)) 
            self.chebet = [[Raise(self.min), self.valuebet], [Call(), brain.pot], [Fold()]]
            self.dealbet = [[Call(), min(40, brain.stack/10)], [Fold(), brain.pot], [Fold()]]          
            self.betrai = [[Call(), min(40, brain.stack/10)], [Fold, self.oppallin], [Fold()]] 
            self.chebetrai = [[Call(), 30], [Fold, self.oppallin], [Fold()]] 
            self.betrairai = [[Call(), self.myallin/3], [Fold(), self.oppallin], [Fold()]]
            if brain.opp_stats['CHBR']> .2:
                self.chebetrai = [[Call(), min(brain.stack/5, 100)], [Fold(), self.oppallin], [Fold()]]
            if brain.opp_stats['AF']> 1:
                self.betrai = [[Call(), 50], [Call(), 70], [Fold()]]
        elif self.eq == 4: ##91
            self.fir = Bet(randint(20,30)) 
            self.che = Bet(randint(20,30)) 
            self.chebet = [[Raise(self.min), self.valuebet*2], [Call(), self.oppallin], [Call()]]
            self.dealbet = [[Raise(self.min*1.5), 30], [Raise(self.min), 80], [Call()]]          
            self.betrai = [[Raise(self.myallin), self.oppallin], [Raise(self.myallin), self.oppallin], [Call()]] 
            self.chebetrai = [[Raise(self.myallin), self.myallin/2], [Raise(self.myallin), self.oppallin], [Raise(self.myallin)]] 
            self.betrairai = [[Call(), self.myallin/2], [Fold(), self.oppallin], [Fold()]]
            if brain.opp_stats['AF']> 1.5:
                self.fir = Check()
                self.chebet = [[Call(), self.valuebet*2], [Call(), self.oppallin], [Call()]]
                self.dealbet = [[Call(), 40], [Call(), self.oppallin], [Call()]]
                self.chebetrai = [[Call(), self.myallin/2], [Call(), self.oppallin], [Call()]] 
                self.betrairai = [[Call(), self.myallin/2], [Call(), self.myallin*.75], [Call()]]
                           
        else:
            print "turn: umm...", self.eq, brain.ev

    def river(self, brain):
        #it's the river, tell me how to play
        my_action = None
        comm= brain.board.flop()+ (brain.board.turn(),)+ (brain.board.river(),)
        turn= brain.board.turn()
        river= brain.board.river()
        S= False

        if self.eq==1:   ##50
            if brain.opp_stats['AF']< .5:
                S = sum([river.rank>=12 for i in comm])
            if S:
                self.fir = Bet(randint(15,25))
                self.che = Bet(randint(20,32))   
                self.betrai = [[Fold(), 10], [Fold(),self.oppallin],[Fold()]]
                self.dealbet = [[Call(), 20], [Fold(), self.oppallin], [Fold()]]
                self.chebet = [[Call(), 6], [Fold(), self.oppallin], [Fold()]]                 
                self.chebetrai = [[self.randaction(Call(), Fold(), brain.opp_stats['CHBR']*100), 65], [Fold(), self.oppallin], [Fold()]]  



        if self.eq == 0: ##0
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1: ##50
            self.fir = Check()
            self.che = Check() 
            self.betrai = [[Fold(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), randint(8,13)], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), randint(8,13)], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]
            if brain.opp_stats['AF']< .7:
                self.fir = self.randaction(Bet(randint(8,17)), Check(), 50)
                self.che = self.randaction(Bet(randint(8,17)), Check(), 50)           
        elif self.eq == 2: ##70
            self.fir = Bet(randint(10,21))
            self.che = Bet(randint(10,21))
            self.betrai = [[Call(), 40], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), 30], [self.randaction(Call(),Fold(), 50), 31], [Fold()]]
            self.chebet = [[Call(), brain.bb*10], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Call(), 40], [Fold(), self.oppallin], [Fold()]]
            if brain.opp_stats['CHBR']> .2:
                self.chebetrai = [[Call(), 27], [Fold(), 34], [Fold()]]
        elif self.eq == 3: ##80
            self.fir = Bet(randint(12,20)) 
            self.che = Bet(randint(12,20)) 
            self.chebet = [[Raise(self.min), self.valuebet], [Call(), brain.pot], [Fold()]]
            self.dealbet = [[Call(), 40], [Fold(), brain.pot], [Fold()]]          
            self.betrai = [[Call(), 40], [Fold, self.oppallin], [Fold()]] 
            self.chebetrai = [[Call(), 30], [Fold, self.oppallin], [Fold()]] 
            self.betrairai = [[Call(), self.myallin/3], [Fold(), self.oppallin], [Fold()]]
            if brain.opp_stats['CHBR']> .2:
                self.chebetrai = [[Call(), min(brain.stack/5, 100)], [Fold(), 200], [Fold()]]
            if brain.opp_stats['AF']> 1:
                self.betrai = [[Call(), 50], [Call(), 70], [Fold()]]
        elif self.eq == 4: ##95
            self.fir = Bet(randint(40,50)) 
            self.che = Bet(randint(20,30)) 
            self.chebet = [[Raise(self.min), self.valuebet*2], [Call(), self.oppallin], [Call()]]
            self.dealbet = [[Raise(self.myallin), 30], [Raise(self.myallin), 80], [Call()]]
            self.betrai = [[Raise(self.myallin), self.oppallin], [Raise(self.myallin), self.oppallin], [Call()]] 
            self.chebetrai = [[Raise(self.myallin), self.myallin/2], [Raise(self.myallin), self.oppallin], [Raise(self.myallin)]] 
            self.betrairai = [[Raise(self.myallin), self.myallin/2], [Raise(self.myallin), self.oppallin], [Raise(self.myallin)]]

        else:
            print "river: umm...", self.eq, brain.ev
