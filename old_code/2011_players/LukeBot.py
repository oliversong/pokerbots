from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from pokerbots.player.ourbot import *
from random import randint

class LukesDerby(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "LukesDerby"
        self.bot = LukeBot()
        self.bot.eq_ranges = [[20, 47, 87, 93]]*4

class LukesDerby1(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "LukesDerby1"
        self.bot = LukeBot()
        self.bot.eq_ranges = [[23, 61, 72, 91]]*4

class LukesDerby2(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "LukesDerby2"
        self.bot = LukeBot()
        self.bot.eq_ranges = {0: [20, 30, 70, 80], 1: [15, 30, 40, 60], 2: [25, 40, 50, 55], 3: [25, 75, 75, 95]}

class LukesDerby3(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "LukesDerby3"
        self.bot = LukeBot()
        self.bot.eq_ranges = {0: [20, 45, 65, 80], 1: [10, 15, 30, 50], 2: [5, 25, 25, 90], 3: [15, 15, 25, 80]}

class LukesDerby4(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "LukesDerby4"
        self.bot = LukeBot()
        self.bot.eq_ranges = {0: [20, 25, 45, 90], 1: [25, 30, 35, 75], 2: [30, 40, 65, 75], 3: [15, 20, 70, 90]}

class LukesDerby5(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "LukesDerby5"
        self.bot = LukeBot()
        self.bot.eq_ranges = {0: [25, 40, 85, 95], 1: [5, 20, 35, 55], 2: [5, 15, 20, 80], 3: [15, 25, 30, 95]}

class LukesDerby6(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "LukesDerby6"
        self.bot = LukeBot()
        self.bot.eq_ranges = {0: [55, 60, 80, 90], 1: [30, 45, 65, 75], 2: [40, 55, 80, 85], 3: [10, 50, 65, 80]}

class LukesDerby7(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "LukesDerby7"
        self.bot = LukeBot()
        self.bot.eq_ranges = {0: [25, 35, 35, 95], 1: [5, 10, 25, 45], 2: [15, 25, 65, 85], 3: [25, 30, 65, 80]}

class LukesDerby8(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "LukesDerby8"
        self.bot = LukeBot()
        self.bot.eq_ranges = {0: [25, 35, 60, 65], 1: [10, 20, 30, 50], 2: [15, 30, 40, 80], 3: [35, 40, 60, 90]}

class LukeBot:
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        # my name
        self.name = "lukebot"
        self.hand = None
        self.stack = None
        self.pip = None
        self.button = None
        self.opponent = None
        self.bb = None
        self.sb = None
        self.hands_played = None
        self.board = None
        self.legal = None
        self.actions = None
        self.last = None
        self.pot = None
        self.learning = True
        ##Eq ranges for each street
        self.eq_ranges = {PREFLOP:[20, 40, 50, 60],FLOP:[20, 40, 50, 60],TURN:[20, 40, 50, 60],RIVER:[20, 40, 50, 60]}
        self.che = 0                         ##SB calls
        self.fir = 0                         ##on SB
        self.chebet = [[0,0],[0,0],[0,0]]    ##BB raise after call
        self.dealbet = [[0,0],[0,0],[0,0]]   ##SB raise
        self.chebetrai = [[0,0],[0,0],[0,0]] ##Our opponent Check raises us
        self.betrai = [[0,0],[0,0],[0,0]]    ##We bet then our opponent raises
        self.betrairai = [[0,0],[0,0],[0,0]] ##We raise from sb then bb re-raises


    def parameterize(self, equity,street):
        #return min(int(equity*100)/20,4)
        ev = equity*100
        for i,eq in enumerate(self.eq_ranges[street]):
            if ev < eq:
                return i
        return i+1        

    def respond(self, brain):
        """Based on your game state variables (see the __init__), make a
        decision and return an action. If you return an illegal action, the
        engine will automatically fold you
        """
        self.action = []
        for act in brain.actions[-3:]:
            act_type = brain.classify(act[1])
            self.action.append((act_type,0 if act_type not in [RAISE,BET] else act[1].amount))
            
        if not brain.board.flop():
            street = PREFLOP
        elif not brain.board.turn():
            street = FLOP
        elif not brain.board.river():
            street = TURN
        else:
            street = RIVER

        self.che = 0                         ##SB calls
        self.fir = 0                         ##on SB
        self.chebet = [[0,0],[0,0],[0,0]]    ##BB raise after call
        self.dealbet = [[0,0],[0,0],[0,0]]   ##SB raise
        self.chebetrai = [[0,0],[0,0],[0,0]] ##Our opponent Check raises us
        self.betrai = [[0,0],[0,0],[0,0]]    ##We bet then our opponent raises
        self.betrairai = [[0,0],[0,0],[0,0]] ##We raise from sb then bb re-raises
        self.eq = self.parameterize(brain.ev,street)
        self.min = max(brain.opponent['pip']*2,brain.bb)
        self.oppmin = max(brain.pip*2,brain.bb) 
        if self.action[-1][0] in [POST,DEAL] or self.action[-2][0] in [POST,DEAL]:
            self.myallin = brain.stack+brain.pip
            self.oppallin = brain.opponent['stack'] + brain.opponent['pip']
            if brain.ev<0.5:
                self.valuebet = max(brain.pot/2, brain.bb*3) 
            else:
                self.valuebet = max(brain.pot,brain.bb*4,(brain.pot-brain.pot*brain.ev)/(brain.ev))

        if not brain.board.flop():
            self.preflop(brain)
        elif not brain.board.turn():
            self.flop(brain)
        elif not brain.board.river():
            self.turn(brain)
        else:
            self.river(brain)
        
        if brain.hands_played_against > 20 and self.learning:
            self.statoverride(brain)
        
        my_action = self.nextaction(brain,street)
        if DEBUG: print "taking action",my_action, "from the ",street
        # Check that our action is legal
        for action in brain.legal:
            if isinstance(action,type(my_action)):
                break
        else:
            if isinstance(my_action, Raise): #see if we can bet if we can't raise
                for action in brain.legal:
                    if isinstance(action,Bet):
                        my_action = Bet(my_action.amount)
                        break
                else:
                    for action in brain.legal:
                        if isinstance(action,Call): #otherwise see if we can bet
                            my_action = Call()
                            break
                    else:
                        my_action = None
            else:
                my_action = None
        # check fold if we selected no action
        if my_action == None:
            for action in brain.legal:
                if isinstance(action, Check):
                    my_action = action
                    break
            else:
                my_action = Fold()

        action = brain.classify(my_action)
        if action in [RAISE,BET]:
            if my_action.amount < self.min:
                my_action.amount = self.min
            if my_action.amount > brain.stack + brain.pip:
                my_action.amount = brain.stack + brain.pip
#                for action in brain.legal:
#                    if isinstance(action, Call):
#                        my_action = action
#                        break
#                else:
#                    my_action = Check()
                        
        if DEBUG: print "taking action",my_action
        return my_action
    
##########List of Possible Actions we could be facing####################
    def nextaction(self, brain, street):
        if self.action[-1][0] == DEAL or self.action[-1][0] == POST:           ##First to Act
            return self.fir
        elif self.action[-1][0] == CHECK or (self.action[-1][0] == CALL and street == 0):              ##After opponent Check
            return self.che
        elif self.action[-1][0] == BET or (self.action[-1][0] == RAISE and street == 0 and self.action[-2][0] != RAISE):                 ##After opponent Bets
            if self.action[-2][0] == CHECK or (self.action[-2][0] == CALL and street == 0):
                if self.action[-1][1] <= self.chebet[0][1]:
                    return self.chebet[0][0]
                elif self.action[-1][1] <= self.chebet[1][1]:
                    return self.chebet[1][0]
                else:
                    return self.chebet[2][0]

            elif self.action[-2][0] == DEAL or (self.action[-2][0] == POST  and street == 0):
                if self.action[-1][1] <= self.dealbet[0][1]:
                    return self.dealbet[0][0]
                elif self.action[-1][1] <= self.dealbet[1][1]:
                    return self.dealbet[1][0]
                else:
                    return self.dealbet[2][0]
            else:
                if DEBUG: print("What the Fuck!1")
                return None
                
        elif self.action[-1][0] == RAISE:               ##After Opponent Raises
            if self.action[-2][0] == BET:
                if self.action[-3][0] == DEAL:
                    if self.action[-1][1] <= self.betrai[0][1]:
                        return self.betrai[0][0]
                    elif self.action[-1][1] <= self.betrai[1][1]:
                        return self.betrai[1][0]
                    else:
                        return self.betrai[2][0]
                
                elif self.action[-3][0] == CHECK:
                    if self.action[-1][1] <= self.chebetrai[0][1]:
                        return self.chebetrai[0][0]
                    elif self.action[-1][1] <= self.chebetrai[1][1]:
                        return self.chebetrai[1][0]
                    else:
                        return self.chebetrai[2][0]  
            elif self.action[-2][0] == RAISE:           ##This occurrs after a re-raise At this point we should call, fold or go all in, please no re-re-raises that arent all in
                if self.action[-1][1] <= self.betrairai[0][1]:
                    return self.betrairai[0][0]
                elif self.action[-1][1] <= self.betrairai[1][1]:
                    return self.betrairai[1][0]
                else:
                    return self.betrairai[2][0]
            else:
                if DEBUG: print("What the Fuck!??")
                return None
        else:                           ##Impossible
            if DEBUG: print "What the Fuck!123", self.action[-1]  
            return None

    def randaction(self, action1,action2,firstodd):
        if randint(0,99)<firstodd:
            return action1
        else:
            return action2

    def statoverride(self,brain):
        ##If our opponent folds to three bets        
        if not brain.board.flop() and brain.opp_stats['F3B']>0.75:
            if brain.ev < 0.20: ##0
                self.dealbet = [[Fold(), brain.bb*5], [Fold(), brain.bb*10], [Fold()]]
                self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]
            elif brain.ev < 0.40: ##20
                self.dealbet = [[Raise(self.min*2), brain.bb*5], [Raise(self.min), brain.bb*10], [Fold()]]
                self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]
            elif brain.ev < 0.60: ##40
                self.dealbet = [[Raise(self.min*2), brain.bb*5], [Raise(self.min), brain.bb*15], [Fold()]]
                self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]
            elif brain.ev < 0.90: ##60
                self.dealbet = [[Raise(self.min*2), brain.bb*10], [Raise(self.min), brain.bb*20], [Fold()]]
                self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]         
            else: ##90
                self.dealbet = [[Raise(self.min*2), brain.bb*10], [Raise(self.min), brain.bb*20], [Call()]]
                self.betrairai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]
            brain.opp_hand = max(10.0,(1-brain.opp_stats['F3B'])*100)
            if DEBUG: print 'F3B', brain.opp_stats['F3B']
            
        ##If out opponent folds to Steals
        if not brain.board.flop() and brain.opp_stats['FBB']>0.70:
            if brain.ev < 0.20:##0
                self.fir = Raise(brain.bb*3)
                self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]
            elif brain.ev < 0.40: ##20
                self.fir = Raise(brain.bb*3)
                self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]
            elif brain.ev < 0.60: ##40
                self.fir = Raise(brain.bb*3)
                self.betrairai = [[Call(), brain.bb*6], [Fold(), self.oppallin], [Fold()]]
            elif brain.ev < 0.90: ##60
                self.fir = Raise(brain.bb*3)
                self.betrairai = [[Call(), brain.bb*15], [Fold(), self.oppallin], [Fold()]]   
            else: ##90
                self.fir = Raise(brain.bb*3)
                self.betrairai = [[Call(), self.oppallin], [Fold(), self.oppallin], [Fold()]]
            brain.opp_hand = max(10.0, (1-brain.opp_stats['FBB'])*100)
            print 'fbb', brain.opp_stats['FBB']

        #if not brain.board.flop() and brain.opp_stats['LMP'] > 0.75 and self.acion[-1][0]==CALL:
        #    if brain.ev < (1-brain.opp_stats['LMP']+0.1+brain.opp_stats['ST']):
        #        self.che = Check()
        #    else:
        #        self.che = Raise(brain.bb*3)
                
        ##Setting the minimum EV for our opponent
#        if not brain.board.flop():
#            CurrentEV= brain.opp_hand
#            brain.opp_hand = min(CurrentEV,(brain.opp_stats['LMP']+brain.opp_stats['ST'])*100)

        ##Setting the minimum EV for our opponent

        if brain.board.flop() and not brain.board.river() and brain.opp_stats['CHBR'][2] < 0.25:
            if brain.ev < 0.40: ##0
                self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]] 
            elif brain.ev < 0.60: ##40                
                self.chebetrai = [[Call(), brain.bb*3], [Fold(), self.oppallin], [Fold()]]                 
            elif brain.ev < 0.80: ##60               
                self.chebetrai = [[Call(), brain.bb*6], [Fold(), self.oppallin], [Fold()]]
            elif brain.ev < 0.90: ##80
                self.chebetrai = [[Raise(self.min), 12], [Call(), 24], [Fold()]]                    
            else: ##90
                self.chebetrai = [[Raise(self.min*2), 12], [Raise(self.min), 24], [Call()]]                                
            if DEBUG: print 'chbr on turn'
        elif brain.board.river() and brain.opp_stats['CHBR'][3] < 0.25:
            if brain.ev < 0.40: ##0
                self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]] 
            elif brain.ev < 0.60: ##40                
                self.chebetrai = [[Fold(), brain.bb*3], [Fold(), self.oppallin], [Fold()]]                 
            elif brain.ev < 0.80: ##60               
                self.chebetrai = [[Fold(), brain.bb*6], [Fold(), self.oppallin], [Fold()]]
            elif brain.ev < 0.90: ##80
                self.chebetrai = [[Call(), 20], [Fold(), 24], [Fold()]]                    
            else: ##90
                self.chebetrai = [[Raise(self.min*2), 20], [Raise(self.min), 40], [Call()]]
            if DEBUG: print 'chbr on river'

        ##If the opponent goes all in frequently
        if brain.opp_stats['HAI'] > 0.05 and not brain.board.flop():
            if brain.ev < (1-(0.8*brain.opp_stats['HAI'])):
                #self.fir = Raise(8)
                #self.che = Raise(8)
                self.betrairai = [[Call(), 20], [Fold(), self.oppallin], [Fold()]]                    
                self.dealbet = [[Call(), 10], [Fold(), self.oppallin], [Fold()]]
            else:
                #self.fir = Raise(8)
                #self.che = Raise(8)
                self.chebet = [[Raise(self.min), brain.bb*5], [Call(), self.oppallin], [Call()]]
                self.betrairai = [[Call(), 20], [Call(), self.oppallin], [Call()]]
            print "hai",brain.opp_stats['HAI']
                  
    def preflop(self, brain):
        #it's preflop, tell me how to play
        my_action = None
        if self.eq == 0:
            self.fir = Call()
            self.che = Check()
        elif self.eq == 1:
            self.fir = Call()
            self.che = Raise(8)
            self.chebet = [[Fold(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Call(), self.min], [Fold(), self.oppallin], [Fold()]]
            self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]
        elif self.eq == 2:
            self.fir = Call()
            self.che = Raise(8)
            self.chebet = [[Raise(8), 4], [Call(), 8], [Fold()]]
            self.dealbet = [[Call(), 4], [Fold(), self.valuebet], [Fold()]]
            self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]  
        elif self.eq == 3:
            self.fir = Call()
            self.che = Raise(8)
            self.chebet = [[Raise(self.min), 6], [Call(), 10], [Fold()]]
            self.dealbet = [[Raise(self.min), 6], [Call(), 10], [Fold()]]      
            self.betrairai = [[Call(), 10], [Fold(), self.oppallin], [Fold()]]    
        elif self.eq == 4:
            self.fir = Call()
            self.che = Check()
            self.chebet = [[Call(), self.oppallin/10], [Raise(self.min), self.oppallin/4], [Call()]]
            self.dealbet = [[Raise(self.min), self.oppallin/10], [Raise(self.min), self.oppallin/4], [Call()]]
            self.betrairai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]
        elif DEBUG:
            print "flop: umm...", self.eq, brain.ev

###########Strategy to Take On Flop###################
    def flop(self, brain):
        #it's the flop, tell me how to play
        my_action = None
        if self.eq == 0:
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1:
            self.fir = self.randaction(Check(),Bet(self.min),50)
            self.che = Check()    
            self.betrai = [[Call(), self.valuebet], [Fold(),self.oppallin],[Fold()]]
            self.dealbet = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold(), self.oppmin], [Fold(), self.oppallin], [Fold()]]                 
        elif self.eq == 2:
            self.fir = self.randaction(Check(),Bet(self.valuebet),50)
            self.che = Bet(self.valuebet)
            self.chebet = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Raise(self.min), self.valuebet/3], [Call(), self.valuebet], [Fold()]]            
            self.betrai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]] 
            self.chebetrai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]] 
            self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]                 
        elif self.eq == 3:
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min), self.valuebet/3], [Call(), self.valuebet], [Fold()]]
            self.dealbet = [[Raise(self.min), self.valuebet/2], [Call(), self.valuebet], [Fold()]]            
            self.betrai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]] 
            self.chebetrai = [[Call(), self.valuebet], [Fold, self.oppallin], [Fold()]] 
            self.betrairai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]                   
        elif self.eq == 4:
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Call(), self.oppallin/10], [Raise(self.min), self.oppallin/4], [Call()]]
            self.dealbet = [[Raise(self.min), self.oppallin/10], [Raise(self.min), self.oppallin/4], [Call()]]            
            self.betrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]] 
            self.chebetrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]] 
            self.betrairai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]      
        elif DEBUG:
            print "flop: umm...", self.eq, brain.ev

#############Action to Take on Turn###################
    def turn(self, brain):
        #it's the turn, tell me how to play
        my_action = None
        if self.eq == 0:
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1:
            self.fir = self.randaction(Check(),Bet(self.min),50)
            self.che = Check()    
            self.betrai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]                 
            self.chebetrai = [[Fold, self.oppmin], [Fold(), self.oppallin], [Fold()]]                 
        elif self.eq == 2:
            self.fir = self.randaction(Check(),Bet(self.valuebet),50)
            self.che = Bet(self.valuebet)
            self.chebet = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Raise(self.min), self.valuebet/3], [Call(), self.valuebet], [Fold()]]            
            self.betrai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]] 
            self.chebetrai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]] 
            self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]                 
        elif self.eq == 3:
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min), self.valuebet/3], [Call(), self.valuebet], [Fold()]]
            self.dealbet = [[Raise(self.min), self.valuebet/2], [Call(), self.valuebet], [Fold()]]            
            self.betrai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]] 
            self.chebetrai = [[Call(), self.valuebet], [Fold, self.oppallin], [Fold()]] 
            self.betrairai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]                   
        elif self.eq == 4:
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Call(), self.oppallin/10], [Raise(self.min), self.oppallin/4], [Call()]]
            self.dealbet = [[Raise(self.min), self.oppallin/10], [Raise(self.min), self.oppallin/4], [Call()]]            
            self.betrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]] 
            self.chebetrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]] 
            self.betrairai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]      
        elif DEBUG:
            print "turn: umm...", self.eq, brain.ev


    def river(self, brain):
        #it's the river, tell me how to play
        my_action = None
        if self.eq == 0:
            self.fir = Check()
            self.che = Check()
        elif self.eq == 1:
            self.fir = self.randaction(Check(),Bet(self.min),50)
            self.che = Check()    
            self.betrai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.chebet = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.chebetrai = [[Fold, self.oppmin], [Fold(), self.oppallin], [Fold()]]
        elif self.eq == 2:
            self.fir = self.randaction(Check(),Bet(self.valuebet),50)
            self.che = Bet(self.valuebet)
            self.chebet = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.dealbet = [[Raise(self.min), self.valuebet/3], [Call(), self.valuebet], [Fold()]]
            self.betrai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.chebetrai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]
            self.betrairai = [[Fold(), self.oppallin], [Fold(), self.oppallin], [Fold()]]
        elif self.eq == 3:
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Raise(self.min), self.valuebet/3], [Call(), self.valuebet], [Fold()]]
            self.dealbet = [[Raise(self.min), self.valuebet/2], [Call(), self.valuebet], [Fold()]]
            self.betrai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
            self.chebetrai = [[Call(), self.valuebet], [Fold, self.oppallin], [Fold()]]
            self.betrairai = [[Call(), self.valuebet], [Fold(), self.oppallin], [Fold()]]
        elif self.eq == 4:
            self.fir = Bet(self.valuebet)
            self.che = Bet(self.valuebet)
            self.chebet = [[Call(), self.oppallin/10], [Raise(self.min), self.oppallin/4], [Call()]]
            dealbet = [[Raise(self.min), self.oppallin/10], [Raise(self.min), self.oppallin/4], [Call()]]
            self.betrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]
            self.chebetrai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]
            self.betrairai = [[Call(), self.oppallin], [Call(), self.oppallin], [Call()]]
        elif DEBUG:
            print "river: umm...", self.eq, brain.ev

class LukeBotNew(LukeBot):
    def __init__(self):
        LukeBot.__init__(self)
        self.name = "LukeBotNew"
    def statoverride(self,brain):
        LukeBot.statoverride(self,brain)
        if not brain.board.flop():
            CurrentEV= brain.opp_hand
            if brain.button:
                brain.opp_hand = min(CurrentEV,max(brain.opp_stats['HPFBB']*100.0,1))
            else:
                brain.opp_hand = min(CurrentEV,max(brain.opp_stats['HPFSB']*100.0,1))


