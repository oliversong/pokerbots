from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from pokerbots.player.ourbot import CHECK, BET, RAISE, FOLD, CALL, DEAL, SHOW, WON, POST, PREFLOP, FLOP, TURN, RIVER, DEBUG
from random import randint

#class TheDerbs8(TheBostonDerby):
#    def __init__(self):
#        TheBostonDerby.__init__(self)
#        self.name = "TheDerbs8"
#        self.bot = basebot8()

class basebot8:
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
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
        # my name
        self.name = "basebot"
        
        self.pfeq = 0   #value between 0 and 4 to indicate what range
                        # our preflop equity was in. 0 = 0-20%, 1=20-40%, etc
        self.my_last_action = {'action':FOLD, 'first':False, 'reraise':False, 'street':PREFLOP, 'betfromaf':False, 'amount':0}
        
        self.eq_ranges = [20, 40, 50, 60]


    def parameterize(self, equity):
        #return min(int(equity*100)/20,4)
        ev = equity*100
        for i,eq in enumerate(self.eq_ranges):
            if ev < eq:
                return i
        return i+1
        
    def hand_confidence(self,brain):
        stack_size = brain.stack + brain.pip
        brain.bound = stack_size
        if not brain.board.flop():
            if stack_size < 30*brain.bb:
                if brain.ev < .7: #if small stack, and not one of best hands
                    brain.bound = 0 # fold
                else:
                    brain.bound = -1
            else:
                if brain.ev > .9:# or (brain.stats['pfhb'] > 0.25 and brain.hands_played > 12):
                    brain.bound = stack_size
                elif brain.ev > .8:
                    brain.bound = int(HIGH * stack_size)
                elif brain.ev > .5:
                    brain.bound = 5 * brain.bb
                else:
                    brain.bound = brain.bb
        else:
            if brain.ev < .33:
                brain.bound = min(int(max(brain.pot*brain.ev/(1-3*brain.ev),0)),stack_size)


    def respond(self, brain):
        """Based on your game state variables (see the __init__), make a
        decision and return an action. If you return an illegal action, the
        engine will automatically fold you
        """
        self.min_bet = max(2*brain.opponent['pip'],self.bb)
        if not brain.board.flop():
            self.pfeq = self.parameterize(brain.ev)
            my_action = self.preflop(brain)
            self.my_last_action['street'] = PREFLOP
            if DEBUG: print "taking action",my_action, "from the preflop"
        elif not brain.board.turn():
            my_action = self.flop(brain)
            self.my_last_action['street'] = FLOP
            if DEBUG: print "taking action",my_action, "from the flop"
        elif not brain.board.river():
            my_action = self.turn(brain)
            self.my_last_action['street'] = TURN
            if DEBUG: print "taking action",my_action, "from the turn"
        else:
            my_action = self.river(brain)
            self.my_last_action['street'] = RIVER
            if DEBUG: print "taking action",my_action, "from the river"
            
        # Check that our action is legal
        for action in brain.legal:
            if isinstance(action,type(my_action)):
                break
        else:
            if isinstance(my_action, Raise):
                for action in brain.legal:
                    if isinstance(action,Call):
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

        self.hand_confidence(brain)
        self.my_last_action['first'] = self.first
        action = brain.classify(my_action)
        if action in [RAISE,BET]:
            if brain.bound == -1:
                my_action.amount = brain.pip+brain.stack
            else:
                my_action.amount = int(min(my_action.amount, brain.bound))
                if my_action.amount < self.min_bet:
                    for action in brain.legal:
                        if isinstance(action, Call):
                            my_action = action
                            self.my_last_action['amount'] = brain.opponent['pip']
                            break
                    else:
                        my_action = Check()
                            
                else:
                    self.my_last_action['amount'] = my_action.amount
        if isinstance(my_action, Call): #should we really call here?
            bet = brain.opponent['pip']
            if (bet-brain.pip)/float(brain.pot + 2*bet) >= brain.ev: #pot odds greater than ev, so fold
                my_action = Fold()
                #print "was going to call!"
            else:
                self.my_last_action['amount'] = brain.opponent['pip']
        self.my_last_action['action'] = brain.classify(my_action)
        if DEBUG: print "taking action",my_action
        return my_action
    
    def new_hand(self):
        self.my_last_action = {'action':FOLD, 'first':False, 'reraise':False, 'street':PREFLOP, 'betfromaf':False, 'amount':0}
    
    def preflop(self, brain):
        #it's preflop, tell me how to play
        last_act = brain.actions[-1]
        last_action = brain.classify(last_act[1])
        if DEBUG: print "opp last action was",last_act, "and pfeq is", self.pfeq
        if DEBUG: print "legal actions:", brain.legal
        self.first = last_action == POST
        stack_size = brain.pip+brain.stack
        my_action = None
        
        if self.pfeq == 0:
            if self.first:
                my_action = Call()
            if last_action == RAISE:
                my_action = Fold()
            else:
                my_action = Check()
        elif self.pfeq == 1:
            if self.first:
                my_action = Call()
            elif last_action == CALL:
                my_action = Raise(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size))) #low-mid
            elif last_action == RAISE:
                if self.my_last_action['action'] == CHECK or last_act[1].amount/float(stack_size) > brain.LOW: #TODO: this should be pot odds!
                    my_action = Fold()
                else:
                    my_action = Call()
        elif self.pfeq == 2:
            if self.first:
                my_action = Raise(brain.LOW*stack_size)
            elif last_action == CALL:
                my_action = Raise(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size))) #low to mid
            elif last_action == RAISE:
                if self.my_last_action['action'] == CHECK or last_act[1].amount/float(stack_size) > brain.MID:
                    my_action = Fold()
                else:
                    my_action = Call()
        elif self.pfeq == 3:
            if self.first:
                my_action = Raise(brain.LOW*stack_size)
            elif last_action == CALL:
                my_action = Raise(brain.MID*stack_size)
            elif last_action == RAISE:
                if self.my_last_action['action'] == CHECK or last_act[1].amount/float(stack_size) > brain.MID:
                    my_action = Fold()
                else:
                    my_action = Call()
        elif self.pfeq == 4:
            if self.first or last_action == RAISE:
                if self.my_last_action['action'] == RAISE:
                    if self.my_last_action['reraise']:
                        my_action = Raise(stack_size)
                    else:
                        my_action = Raise(self.min_bet)
                        self.my_last_action['reraise'] = True
                else:
                    my_action = Raise(brain.MID*stack_size)
            elif last_action == CALL:
                my_action = Raise(brain.LOW*stack_size)
        else:
            print "preflop: umm...", self.pfeq, brain.ev
        if DEBUG: print "and action",my_action
        return my_action
    
    def flop(self, brain):
        #it's the flop, tell me how to play
        last_act = brain.actions[-1]
        last_action = brain.classify(last_act[1])
        if DEBUG: print "opp last action was",last_act, "and pfeq is", self.pfeq
        if DEBUG: print "legal actions:", brain.legal
        self.first = last_action == DEAL
        stack_size = brain.pip+brain.stack

        my_action = None
        eq = self.parameterize(brain.ev)
        if self.pfeq == 0:
            if eq == 0:
                if self.first or last_action == CHECK:
                    my_action = Check()
                elif last_action in [BET, RAISE]:
                    my_action = Fold()
            elif eq == 1:
                if self.first:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(self.min_bet)
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action in [BET, RAISE]:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 2:
                if brain.opp_stats['AF'] < .5:
                    for action in brain.legal:
                        if isinstance(action,Raise) or isinstance(action,Bet):
                            my_action = action
                            self.my_last_action['betfromaf'] = True
                            break
                elif self.first:
                    my_action = Bet(brain.LOW*stack_size)
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(brain.LOW*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_act = Call()
                        elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                            if brain.opp_stats['INCR'] < .2 : #or brain.opp_stats['CHBR'] < .4
                                my_action = Fold()
                            else:
                                my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['betfromaf']:
                        my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount == 2*self.my_last_action['amount']:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 3:
                if self.first or last_action == CHECK:
                    my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size))) #low-mid
                elif last_action == BET:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else: #then I must have bet
                        if last_act[1].amount == 2*self.my_last_action['amount']:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(brain.MID*stack_size),int(brain.HIGH*stack_size))) #mid_high
                elif last_action == CHECK:
                    my_action = Bet(int(brain.LOW*stack_size))
                elif last_action == BET:
                    my_action = Raise(int(brain.MID*stack_size))
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(int(brain.MID*stack_size))
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
        elif self.pfeq == 1:
            if eq == 0:
                if self.first or last_action == CHECK:
                    my_action = Check()
                elif last_action in [BET, RAISE]:
                    my_action = Fold()
            elif eq == 1:
                if self.first:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(randint(self.min_bet,int(brain.LOW*stack_size)))
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action in [BET, RAISE]:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 2:
                if brain.opp_stats['AF'] < .5:
                    for action in brain.legal:
                        if isinstance(action,Raise) or isinstance(action,Bet):
                            my_action = action
                            self.my_last_action['betfromaf'] = True
                            break
                elif self.first:
                    my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size)))
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(brain.LOW*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_act = Call()
                        elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                            if brain.opp_stats['INCR'] < .2 : #or brain.opp_stats['CHBR'] < .4
                                my_action = Fold()
                            else:
                                my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['betfromaf']:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_act = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 3:
                if self.first or last_action == CHECK:
                    my_action = Bet(int(brain.MID*stack_size))
                elif last_action == BET:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_action = Raise(int(brain.MID*stack_size))
                        elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                            my_action = Call()
                        else:
                            my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else: #then I must have bet
                        if last_act[1].amount == 2*self.my_last_action['amount']:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(brain.MID*stack_size),int(brain.HIGH*stack_size))) #mid_high
                elif last_action == CHECK:
                    my_action = Bet(int(brain.LOW*stack_size))
                elif last_action == BET:
                    my_action = Raise(int(brain.MID*stack_size))
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(int(brain.MID*stack_size))
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
        elif self.pfeq == 2:
            if eq == 0:
                if self.first:
                    if brain.opp_stats['AF'] < .5:
                        my_action = Bet(int(brain.MID*stack_size))
                    else:
                        my_action = Check()
                elif last_action == CHECK:
                    my_action = Bet(brain.MID*stack_size)
                elif last_action in [BET, RAISE]:
                    my_action = Fold()
            elif eq == 1:
                if self.first:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(randint(self.min_bet,int(brain.LOW*stack_size)))
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 2:
                if self.first:
                    if brain.opp_stats['AF'] < .5:
                        my_action = Bet(int(brain.MID*stack_size))
                        self.my_last_action['betfromaf'] = True
                    else:
                        my_action = Check()
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 3:
                if self.first or last_action == Check:
                    my_action = Bet(int(brain.MID*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Raise(int(brain.MID*stack_size))
                    elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.HIGH:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount == 2*self.my_last_action['amount']:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action == Call()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(brain.MID*stack_size),int(brain.HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(int(brain.MID*stack_size))
                elif last_action == BET:
                    my_action = Raise(int(brain.MID*stack_size))
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
                    else:
                        my_action = Raise(int(brain.MID*stack_size))
        elif self.pfeq == 3:
            if eq == 0:
                if self.first:
                    if brain.opp_stats['AF'] < .5:
                        my_action = Bet(int(brain.MID*stack_size))
                    else:
                        my_action = Check()
                elif last_action == CHECK:
                    my_action = Bet(int(brain.MID*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    my_action = Fold()
            elif eq == 1:
                if self.first:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(randint(self.min_bet,int(brain.LOW*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(int(brain.LOW*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 2:
                if self.first:
                    if brain.opp_stats['AF'] < .5:
                        my_action = Bet(int(brain.MID*stack_size))
                        self.my_last_action['betfromaf'] = True
                    else:
                        my_action = Bet(int(brain.LOW*stack_size))
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 3:
                if self.first or last_action == Check:
                    my_action = Bet(int(brain.MID*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Raise(int(brain.MID*stack_size))
                    elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Raise(self.min_bet)
                        elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount == 2*self.my_last_action['amount']:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Call()
            elif eq == 4:
                if self.first:
                    my_action = Check()
                elif last_action == CHECK:
                    my_action = Bet(int(brain.LOW*stack_size))
                elif last_action == BET:
                    my_action = Call()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(int(brain.MID*stack_size))
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
        elif self.pfeq == 4:
            if eq == 0:
                if self.first or last_action == CHECK:
                    my_action = Check()
                elif last_action in [BET, RAISE]:
                    my_action = Fold()
            elif eq == 1:
                if self.first or last_action == CHECK:
                    my_action = Bet(int(brain.MID*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if last_act[1].amount == 2*self.my_last_action['amount']:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 2:
                if self.first or last_action == CHECK:
                    my_action = Bet(int(brain.MID*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Raise(int(brain.MID*stack_size))
                    elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Raise(self.min_bet)
                            self.my_last_action['reraise'] = True
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['reraise']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Call()
            elif eq == 3:
                if self.first:
                    my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(int(brain.MID*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Raise(2*self.min_bet)
                    elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.HIGH:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount == 2*self.my_last_action['amount']:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Call()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(brain.MID*stack_size),int(brain.HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(int(brain.LOW*stack_size))
                elif last_action == BET:
                    my_action = Raise(int(brain.MID*stack_size))
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(int(brain.MID*stack_size))
                    else:
                        my_action = Raise(stack_size)
        else:
            print "flop: umm...", self.pfeq, brain.ev
        return my_action

    def turn(self, brain):
        #it's the turn, tell me how to play
        last_act = brain.actions[-1]
        last_action = brain.classify(last_act[1])
        if DEBUG: print "opp last action was",last_act, "and pfeq is", self.pfeq
        if DEBUG: print "legal actions:", brain.legal
        self.first = last_action == DEAL
        stack_size = brain.pip+brain.stack
        my_action = None
        eq = self.parameterize(brain.ev)
        if self.pfeq == 0:
            if eq == 0:
                if self.first:
                    return Check()
                elif last_action == BET:
                    if last_act[1].amount == 2*self.my_last_action['amount']:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == CHECK:
                    #ignoring condition on previous betting
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(brain.MID*stack_size)
                elif last_action == RAISE:
                    my_action = Fold()
            elif eq == 1:
                if brain.opp_stats['AF'] < .5:
                    for action in brain.legal:
                        if isinstance(action,Raise):
                            my_action = Raise(brain.MID*stack_size)
                            self.my_last_action['betfromaf'] = True
                            break
                        elif isinstance(action,Bet):
                            my_action = Bet(brain.MID*stack_size)
                            self.my_last_action['betfromaf'] = True
                            break
                elif self.first:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(randint(self.min_bet,int(brain.LOW*stack_size)))
                elif last_action == CHECK:
                        my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size)))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount == 2*self.my_last_action['amount']:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
            elif eq == 2:
                if brain.opp_stats['AF'] < .5:
                    for action in brain.legal:
                        if isinstance(action,Raise):
                            my_action = Raise(brain.MID*stack_size)
                            self.my_last_action['betfromaf'] = True
                            break
                        elif isinstance(action,Bet):
                            my_action = Bet(brain.MID*stack_size)
                            self.my_last_action['betfromaf'] = True
                            break
                elif self.first:
                    my_action = Bet(brain.LOW*stack_size)
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(brain.LOW*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    elif last_act[1].amount/float(stack_size) <= brain.MID:
                        if brain.opp_stats['AF'] > 1.5:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_action = Call()
                        elif last_act[1].amount/float(stack_size) <= brain.MID:
                            if brain.opp_stats['INCR'] < .2 : #or brain.opp_stats['CHBR'] < .4 or this is a continutation bet
                                my_action = Fold()
                            else:
                                my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['betfromaf']:
                        my_action = Fold()
            elif eq == 3:
                if self.first or last_action == CHECK:
                    my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size)))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if brain.opp_stats['AF'] < .5:
                            my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= brain.MID:
                                my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        #if opp never bet/raised: fold
                        my_action = Call()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(brain.MID*stack_size),int(brain.HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(brain.LOW*stack_size)
                elif last_action == BET:
                    my_action = Bet(brain.MID*stack_size)
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(brain.MID*stack_size)
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
        elif self.pfeq == 1:
            if eq == 0:
                if self.first:
                    return Check()
                elif last_action == BET:
                    if last_act[1].amount == 2*self.my_last_action['amount']:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == CHECK:
                    #ignoring condition on previous betting
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(brain.MID*stack_size)
                elif last_action == RAISE:
                    my_action = Fold()
            elif eq == 1:
                if self.first:
                    if brain.opp_stats['AF'] < .5:
                        for action in brain.legal:
                            if isinstance(action,Raise):
                                my_action = Raise(brain.MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                            elif isinstance(action,Bet):
                                my_action = Bet(brain.MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                    else:
                        if randint(0,99) < 50:
                            my_action = Check()
                        else:
                            my_action = Bet(randint(self.min_bet,int(brain.LOW*stack_size)))
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 2:
                if self.first:
                    if brain.opp_stats['AF'] < .5:
                        for action in brain.legal:
                            if isinstance(action,Raise):
                                my_action = Raise(brain.MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                            elif isinstance(action,Bet):
                                my_action = Bet(brain.MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                    else:
                        my_action = Bet(brain.LOW*stack_size)
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(brain.LOW*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    elif last_act[1].amount/float(stack_size) <= brain.MID:
                        if brain.opp_stats['AF'] > 1.5:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if self.my_last_action['betfromaf']:
                            if last_act[1].amount/float(stack_size) <= brain.MID:
                                my_action = Call()
                            else:
                                my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= brain.LOW:
                                my_action = Call()
                            elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                                if brain.opp_stats['INCR'] < .2 : #or brain.opp_stats['CHBR'] < .4 or this is a continutation bet
                                    my_action = Fold()
                                else:
                                    my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount == 2*self.my_last_action['amount']:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 3:
                if self.first:
                    my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size)))
                elif last_action == CHECK:
                    if stack_size > 1.7*400:
                        my_action = Bet(stack_size)
                    else:
                        my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size)))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Call()
                    elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                        if randint(0,99) < 50:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if brain.opp_stats['AF'] < .5:
                            my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= brain.MID:
                                my_action = Call()
                            else:
                                my_action = Fold()
                    else:
                        #if opp has not raised/bet this hand: fold
                        my_action = Call()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(brain.MID*stack_size),int(brain.HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(brain.LOW*stack_size)
                elif last_action == BET:
                    my_action = Raise(brain.MID*stack_size)
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(brain.MID*stack_size)
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
        elif self.pfeq == 2:
            if eq == 0:
                if self.first:
                    my_action = Check()
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Bet(brain.MID*stack_size)
                    else:
                        my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount == 2*self.my_last_action['amount']:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    my_action = Fold()
            elif eq == 1:
                if self.first:
                    if brain.opp_stats['AF'] < .5:
                        for action in brain.legal:
                            if isinstance(action,Raise):
                                my_action = Raise(brain.MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                            elif isinstance(action,Bet):
                                my_action = Bet(brain.MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                    else:
                        if randint(0,99) < 50:
                            my_action = Check()
                        else:
                            my_action = Bet(randint(self.min_bet,int(brain.LOW*stack_size)))
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    elif last_act[1].amount/float(stack_size) <= brain.MID:
                        if randint(0,99) < 50:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if self.my_last_action['betfromaf']:
                            my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= brain.LOW:
                                my_action = Call()
                            else:
                                my_action = Fold()
            elif eq == 2:
                if self.first:
                    my_action = Bet(brain.MID*stack_size)
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    elif last_act[1].amount/float(stack_size) <= brain.MID:
                        if brain.opp_stats['AF'] > 1.5:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_action = Call()
                        elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                            if brain.opp_stats['INCR'] < .2 : #or brain.opp_stats['CHBR'] < .4 or this is a continutation bet
                                my_action = Fold()
                            else:
                                my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 3:
                if self.first:
                    my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size)))
                elif last_action == CHECK:
                    if stack_size > 1.7*400:
                        my_action = Bet(stack_size)
                    else:
                        my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size)))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Call()
                    elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                        if randint(0,99) < 50:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if brain.opp_stats['AF'] < .5:
                            my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= brain.MID:
                                my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        #if opp has not raised/bet this hand: fold
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(brain.MID*stack_size),int(brain.HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(brain.LOW*stack_size)
                elif last_action == BET:
                    my_action = Raise(brain.MID*stack_size)
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(brain.MID*stack_size)
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
        elif self.pfeq == 3:
            if eq == 0:
                if self.first:
                    my_action = Bet(brain.MID*stack_size)
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Bet(brain.MID*stack_size)
                    else:
                        my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount == 2*self.my_last_action['amount']:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        my_action = Fold()
            elif eq == 1:
                if self.first:
                    if brain.opp_stats['AF'] < .5:
                        for action in brain.legal:
                            if isinstance(action,Raise):
                                my_action = Raise(brain.MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                            elif isinstance(action,Bet):
                                my_action = Bet(brain.MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                    else:
                        if randint(0,99) < 50:
                            my_action = Check()
                        else:
                            my_action = Bet(brain.LOW*stack_size)
                elif last_action == CHECK:
                    my_action = Bet(brain.MID*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if self.my_last_action['betfromaf']:
                            my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= brain.LOW:
                                my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 2:
                if self.first:
                    if stack_size <= .6 * 400:
                        my_action = Check()
                    else:
                        my_action = Bet(brain.MID*stack_size)
                elif last_action == CHECK:
                    my_action = Bet(brain.MID*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Raise(brain.MID*stack_size)
                    elif last_act[1].amount/float(stack_size) <= brain.MID:
                        if brain.opp_stats['AF'] < .5:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_action = Call()
                        elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                            if brain.opp_stats['INCR'] < .2 : #or brain.opp_stats['CHBR'] < .4 or this is a continutation bet
                                my_action = Fold()
                            else:
                                my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_action = Call()
                        elif last_act[1].amount/float(stack_size) <= brain.MID:
                            if stack_size <= .6 * 400:
                                my_action = Fold()
                            else:
                                my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 3:
                if self.first:
                    my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size)))
                elif last_action == CHECK:
                    if stack_size > 1.7*400:
                        my_action = Bet(stack_size)
                    else:
                        my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size)))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Raise(brain.HIGH*stack_size)
                    elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                            if last_act[1].amount/float(stack_size) <= brain.MID:
                                my_action = Call()
                            elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                                if brain.opp_stats['AF'] < .5:
                                    my_action = Fold()
                                else:
                                    my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        #if opp has not raised/bet this hand: fold
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == RAISE:    
                        my_action = Call()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(brain.MID*stack_size),int(brain.HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(brain.LOW*stack_size)
                elif last_action == BET:
                    my_action = Raise(brain.MID*stack_size)
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(brain.MID*stack_size)
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
        elif self.pfeq == 4:
            if eq == 0:
                if self.first or last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 1:
                if self.first:
                    if brain.opp_stats['AF'] < .5:
                        for action in brain.legal:
                            if isinstance(action,Raise):
                                my_action = Raise(brain.MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                            elif isinstance(action,Bet):
                                my_action = Bet(brain.MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                    else:
                        if randint(0,99) < 50:
                            my_action = Check()
                        else:
                            my_action = Bet(randint(int(self.min_bet),int(brain.LOW*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size)))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if self.my_last_action['betfromaf']:
                            my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= brain.LOW:
                                my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 2:
                if self.first:
                    my_action = Bet(brain.MID*stack_size)
                    if brain.opp_stats['AF'] < .5:
                        self.my_last_action['betfromaf'] = True
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(brain.MID*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if self.my_last_action['betfromaf']:
                            if last_act[1].amount/float(stack_size) <= brain.MID:
                                my_action = Call()
                            else:
                                my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= brain.MID:
                                my_action = Call()
                            elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                                if brain.opp_stats['AF'] < .5:
                                    my_action = Fold()
                                else:
                                    my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= brain.LOW:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 3:
                if self.first:
                    my_action = Bet(randint(int(brain.LOW*stack_size),int(brain.MID*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(brain.MID*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_action = Raise(brain.LOW*stack_size)
                    elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                            if brain.opp_stats['AF'] < .5:
                                my_action = Fold()
                            elif last_act[1].amount/float(stack_size) <= brain.MID:
                                my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= brain.HIGH:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == RAISE:    
                        my_action = Call()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(brain.MID*stack_size),int(brain.HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(brain.MID*stack_size)
                elif last_action == BET:
                    my_action = Raise(brain.MID*stack_size)
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Call()
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
        else:
            print "turn: umm...", self.pfeq, brain.ev
        return my_action

    def river(self, brain):
        #it's the river, tell me how to play
        last_act = brain.actions[-1]
        last_action = brain.classify(last_act[1])
        if DEBUG: print "opp last action was",last_act, "and pfeq is", self.pfeq
        if DEBUG: print "legal actions:", brain.legal
        self.first = last_action == DEAL
        stack_size = brain.pip+brain.stack

        my_action = None
        eq = self.parameterize(brain.ev)
        if eq == 2:
            if self.first or last_action == CHECK:
                my_action = Bet(brain.MID*stack_size)
            elif last_action == BET:
                if last_act[1].amount/float(stack_size) <= brain.MID:
                    my_action = Call()
                elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                    if brain.opp_stats['AF'] > 1.5:
                        my_action = Call()
                    else:
                        my_action = Fold()
                else:
                    my_action = Fold()
            elif last_action == RAISE:
                if self.my_last_action['action'] == BET:
                    if last_act[1].amount/float(stack_size) <= brain.LOW:
                        my_act = Call()
                    elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                        if brain.opp_stats['INCR'] < .2 : #or brain.opp_stats['CHBR'] < .4 or cb
                            my_action = Fold()
                        else:
                            my_action = Call()
                    else:
                        my_action = Fold()
        elif eq == 3:
            if self.first or last_action == CHECK:
                my_action = Bet(brain.MID*stack_size)
            elif last_action == BET:
                if last_act[1].amount/float(stack_size) <= brain.MID:
                    my_action = Raise(brain.MID*stack_size)
                elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                    #if opp never raised b4: fold
                    my_action = Call()
                else:
                    my_action = Fold()
            elif last_action == RAISE:
                if self.my_last_action['first']:
                    if brain.opp_stats['AF'] < .5:
                        my_action = Fold()
                    else:
                        if last_act[1].amount/float(stack_size) <= brain.MID:
                            my_action = Call()
                        elif last_act[1].amount/float(stack_size) <= brain.HIGH:
                            #if op never raised in this hand: Fold
                            my_action = Call()
                        else:
                            my_action = Fold()
                if self.my_last_action['action'] == BET:
                    #if opp has not raised this hand: Fold
                    my_action = Call()
        elif eq == 4:
            if self.first:
                if stack_size < 200 or stack_size > 600:
                    my_action = Bet(stack_size)
                else:
                    if randint(0,99) < 50:
                        my_action = Bet(brain.HIGH*stack_size)
                    else:
                        my_action = Bet(brain.MID*stack_size)
            elif last_action == CHECK:
                my_action = Bet(brain.MID*stack_size)
            elif last_action == BET:
                my_action = Raise(brain.MID*stack_size)
            elif last_action == RAISE:
                my_action = Raise(stack_size)
        return my_action
