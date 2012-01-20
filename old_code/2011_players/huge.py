from random import randint
from pokerbots.engine.game import Raise, Check, Call, Bet, Fold, Deal, Show, Won, Post
from collections import deque
from pokereval import PokerEval

LOW = .02
MID = .08
HIGH = .15

CHECK, BET, RAISE, FOLD, CALL, DEAL, SHOW, WON, POST = range(9)
PREFLOP, FLOP, TURN, RIVER = range(4)
DEBUG = False

# hand lookup table. use: to figure out equity of preflop pocket cards T2o,
# just do lookuphand[8][0][1] (card ranks minus 2 are first two indices, and then
# second index is 0 if suited and 1 if off-suit
lookuphand = [
                [#2
                    [-1, 52.6],#2
                    [94.6, 100.00],#3
                    [90.6, 99.1],#4
                    [89.1, 97.3],#5
                    [89.4, 98.2],#6
                    [88.8, 96.4],#7
                    [81.9, 91.6],#8
                    [75.9, 85.5],#9
                    [66.5, 77.7],#10
                    [58.1, 68.6],#J
                    [48.9, 59.0],#Q
                    [37.6, 47.7],#K
                    [22.0, 30.9],#A
                ],
                [#3
                    [-1, 39.2],#3
                    [85.8, 95.5],#4
                    [82.5, 93.4],#5
                    [83.7, 94.3],#6
                    [82.2, 92.5],#7
                    [78.9, 90.3],#8
                    [72.5, 83.4],#9
                    [64.1, 74.7],#10
                    [54.4, 65.3],#J
                    [44.9, 54.1],#Q
                    [34.5, 42.8],#K
                    [18.7, 26.8],#A
                ],
                [#4
                    [-1, 27.3],#4
                    [76.5, 87.6],#5
                    [76.8, 88.5],#6
                    [76.2, 86.7],#7
                    [72.9, 84.6],#8
                    [70.1, 80.7],#9
                    [60.5, 71.0],#10
                    [52.2, 61.7],#J
                    [41.0, 51.9],#Q
                    [32.1, 40.1],#K
                    [17.2, 24.7],#A                
                ],
                [#5
                    [-1, 16.0],#5
                    [71.3, 81.6],#6
                    [69.8, 79.8],#7
                    [66.8, 78.6],#8
                    [63.8, 73.8],#9
                    [59.3, 69.5],#10
                    [49.2, 60.2],#J
                    [38.8, 48.6],#Q
                    [27.6, 36.3],#K
                    [12.8, 19.9],#A                
                ],
                [#6
                    [-1, 9.5],#6
                    [64.4, 75.6],#7
                    [60.8, 72.2],#8
                    [57.8, 67.7],#9
                    [53.2, 63.5],#10
                    [46.5, 57.5],#J
                    [35.4, 45.9],#Q
                    [25.9, 33.9],#K
                    [14.0, 20.8],#A                 
                ],
                [#7
                    [-1, 4.2],#7
                    [54.8, 66.2],#8
                    [52.9, 62.6],#9
                    [46.8, 56.6],#10
                    [40.7, 50.1],#J
                    [34.2, 41.9],#Q
                    [22.3, 30.0],#K
                    [10.7, 18.4],#A                 
                ],
                [#8
                    [-1, 3.2],#8
                    [46.2, 55.7],#9
                    [40.4, 51.0],#10
                    [34.8, 43.7],#J
                    [27.9, 37.3],#Q
                    [19.0, 28.8],#K
                    [12.670, 21.569],#A                 
                ],
                [#9
                    [-1, 2.7],#9
                    [35.1, 44.6],#10
                    [29.1, 38.5],#J
                    [23.5, 31.8],#Q
                    [14.6, 23.2],#K
                    [8.1, 12.5],#A                 
                ],
                [#10
                    [-1, 2.3],#10
                    [23.8, 33.0],#J
                    [17.5, 25.6],#Q
                    [10.4, 16.9],#K
                    [5.7, 9.0],#A                
                ],
                [#J
                    [-1, 1.8],#J
                    [14.3, 21.7],#Q
                    [9.8, 13.7],#K
                    [4.5, 7.5],#A                
                ],
                [#Q
                    [-1, 1.4],#Q
                    [7.8, 11.6],#K
                    [3.8, 6.6],#A                  
                ],
                [#K
                    [-1, 0.9],#K
                    [3.5, 5.4],#A                
                ],
                [#A
                    [-1, 0.5] #A
                ]
            ]
                
class Template:
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        # my name
        self.name = "testbot"

        # game state variables -- these are updated by the engine which
        # own internal representation. so if you modify them, they'll just
        # be reset. we recommend leaving their init as is
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

    def respond(self):
        """Based on your game state variables (see the __init__), make a
        decision and return an action. If you return an illegal action, the
        engine will automatically fold you
        """

        for action in self.legal:
            if isinstance(action, Raise):
                if self.hand[0].rank == self.hand[1].rank:
                    return Raise(self.stack + self.pip)
                return Call()

        for action in self.legal:
            if isinstance(action, Bet):
                if randint(0, 100) < 35:
                    return Bet(self.stack/2)
            return Check()

        return Fold()


class TheBostonDerbyD:
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        # my name
        self.name = "theBostonDerbyD"

        self.stats = {
                        #cumulative stats
                        'hands':0, # number hands played
                        'RaisedPF':0,
                        'RaisedOrCalledPF':0,
                        'AFNumerator':0,
                        'AFDenominator':0,
                        '20RaiseOrCallPF':0,
                        #normalized stats
                        'vpip':0,  # amount voluntarily placed in pot
                        'pfr':0,   # frequency of pre flop raises
                        'af':0,    # aggression frequency = (bets + raises)/(checks + calls)
                        #pre flop
                        'st':0,    # steals = how often he raises when has first action
                        'limp':0,  # how often opponent calls
                        'fb':0,    # how often, after small blind raises, big blind folds
                        '3b':0,    # how often, after small blind raises, big blind raises
                        'f3b':0,   # how often, after small blind raises and then big blind raises, small blind folds
                        '4b':0,    # how often, the small bind raises in above circumstances
                        #post flop
                        'cb':0,    # continuation bet = how often betting after betting/raising on preflop
                        'fcb':0,   # how often opp folds to a continuation bet
                        'cr':0,    # how often opp check raises
                        '2cb':0,   # how often opp cb twice, once on flop and once on turn
                        'f2cb':0,  # how often opp folds to 2nd continuation bet.
                        'pfhb': 0  # how often they call or raise to >= 10% of stack size during pre flop (custom stat)
                     }
                     
        # game state variables -- these are updated by the engine which
        # own internal representation. so if you modify them, they'll just
        # be reset. we recommend leaving their init as is
        self.hand = None
        self.stack = None
        self.pip = None
        self.button = None
        self.opponent = None
        self.bb = None
        self.sb = None
        self.hands_played = None
        self.last_hand = 0
        self.board = None
        self.legal = None
        self.actions = None
        self.last = None
        self.pot = None
        self.ev_calc = PokerEval()
        self.ev = 0
        self.bound = 0
        self.bot = BaseBot()

    def card2str(self, c):
        return c.__str__()

    def calculate_ev(self):
        #print self.board
        if not self.board.flop():
            suited = self.hand[0].suit != self.hand[1].suit #0 means suited, 1 means not
            if self.hand[0].rank > self.hand[1].rank:
                card_2,card_1 = self.hand
            else:
                card_1,card_2 = self.hand
            #print "looking up (%d,%d,%d)" % (card_1.rank-2,card_2.rank-card_1.rank,suited)
            ev = 100.0 - lookuphand[card_1.rank-2][card_2.rank-card_1.rank][suited]
        else:
            board = [self.card2str(c) for c in self.board.flop()]
            if self.board.river():
                board += [self.card2str(self.board.turn()), self.card2str(self.board.river())]
            elif self.board.turn():
                board += [self.card2str(self.board.turn()), '__']
            else:
                board += ['__','__']
            ev = self.ev_calc.poker_eval(game="holdem",pockets=[[self.card2str(c) for c in self.hand],['__','__']],dead=[],board=board,iterations=1000)
            ev = ev['eval'][0]['ev']/10.0
            #this ev assumes we have no knowledge of what our opponent's hand range is!
        self.ev = ev/100.0
    
    def hand_confidence(self):
        stack_size = self.stack + self.pip
        self.bound = stack_size
        if not self.board.flop():
            if stack_size < 30*self.bb:
                if self.ev < .7: #if small stack, and not one of best hands
                    self.bound = 0 # fold
                else:
                    self.bound = -1
            else:
                if self.ev > .9 or (self.stats['pfhb'] > 0.25 and self.hands_played > 12):
                    self.bound = stack_size
                elif self.ev > .8:
                    self.bound = int(HIGH * stack_size)
                elif self.ev > .5:
                    self.bound = 5 * self.bb
                else:
                    self.bound = self.bb
        else:
            if self.ev < .33:
                self.bound = min(int(max(self.pot*self.ev/(1-3*self.ev),0)),stack_size)

    def classify(self, act):
        action = None
        if isinstance(act, Post):
            action = POST
        elif isinstance(act, Check): 
            action = CHECK
        elif isinstance(act, Bet):
            action = BET
        elif isinstance(act, Raise): 
            action = RAISE
        elif isinstance(act, Fold): 
            action = FOLD
        elif isinstance(act, Call): 
            action = CALL
        elif isinstance(act, Show):
            action = SHOW
        elif isinstance(act, Deal): 
            action = DEAL
        elif isinstance(act, Won): 
            action = WON
        else :
            print "umm, unknown action taken!", act
        return action
        

    def calculate_stats(self,last):
        #parse all actions in previous hand into useful information
        if DEBUG: print "calculating stats for hand: ", last
        tallies = {'raises':0, 'bets':0, 'folds':0, 'calls':0, 'checks':0, 'first':False}
        my_actions = dict(zip(range(4),[tallies.copy() for x in range(4)]))
        opp_actions = dict(zip(range(4),[tallies.copy() for x in range(4)]))
        hand = deque(last[:])
        act = hand.popleft() #first action is always sb posting their blind
        my_actions['sb'] = act[0] == self.name
        opp_actions['sb'] = not my_actions['sb'] #if i'm not big blind, opp must be
        hand.popleft() # second action is always bb posting, and is useless

        street = 0 #0 is preflop, 1 is flop, 2 is turn and 3 is river    
        first = True
        while len(hand) > 0 :
            act = hand.popleft()
            #print "parsing action: ",act
            if act[0] == 'Dealer': #then this action corresponds to changing street
                street += 1
                first = True
                continue
            #print "on street: ", street
            action = self.classify(act[1])
            if first and action in [BET, RAISE]:
                first = False
                if act[0] == self.name:
                    my_actions[street]['first'] = True
                elif act[0] == self.opponent['name']:
                    opp_actions[street]['first'] = True
            
            if act[0] == self.name:
                if action == RAISE:
                    my_actions[street]['raises'] += 1
                elif action == CHECK:
                    my_actions[street]['checks'] += 1
                elif action == CALL:
                    my_actions[street]['calls'] += 1
                elif action == FOLD:
                    my_actions[street]['folds'] += 1
                elif action == BET:
                    opp_actions[street]['bets'] += 1
            elif act[0] == self.opponent['name']:
                if street == 0 and action in [RAISE, CALL]:
                    opp_stack = (self.opponent['pip']+self.opponent['stack'])
                    if (action == RAISE and act[1].amount > .1*opp_stack) or \
                        (action == CALL and self.pip > .1 * opp_stack):
                        self.stats['20RaiseOrCallPF'] += 1
                if action == RAISE:
                    opp_actions[street]['raises'] += 1
                elif action == CHECK:
                    opp_actions[street]['checks'] += 1
                elif action == CALL:
                    opp_actions[street]['calls'] += 1
                elif action == FOLD:
                    opp_actions[street]['folds'] += 1
                elif action == BET:
                    opp_actions[street]['bets'] += 1
            else:
                print "unknown player: ",act[0]

        #update relevant statistics
        self.stats['hands'] += 1
        if opp_actions[PREFLOP]['raises'] > 0:
            self.stats['RaisedPF'] += 1
        if opp_actions[PREFLOP]['raises'] > 0 or opp_actions[PREFLOP]['calls'] > 0:
            self.stats['RaisedOrCalledPF'] += 1
        self.stats['AFNumerator'] += sum([opp_actions[x]['raises'] + opp_actions[x]['bets'] for x in [FLOP, TURN, RIVER]])
        self.stats['AFDenominator'] += sum([opp_actions[x]['calls'] for x in [FLOP, TURN, RIVER]])
        '''
        if opp_actions['sb']:
            self.stats['HandsAsSB'] += 1
            if opp_actions[PREFLOP]['raises']: #if he raised as SB, then he attempted to steal the blinds
                if opp_actions[PREFLOP]['first']:
                    self.stats['RaisedPFAsSB'] += 1 #assuming this is it
            elif opp_actions[PREFLOP]['calls']: #if he called instead, then he limped in
                self.stats['CalledPFAsSB'] += 1
        else: # he's BB
            if my_actions[PREFLOP]['raises'] and my_actions[PREFLOP]['first']:
                self.stats['HandsFacingSteal'] += 1
                if opp_actions[PREFLOP]['folds']: #if I first raised as SB and he folded
                    self.stats['FoldedPFAsBB'] += 1
                elif opp_actions[PREFLOP]['raises']:
                    self.stats['ReRaisesPFAsBB']
        '''        
        
        #calculate normalized statistics
        self.stats['vpip'] = self.stats['RaisedOrCalledPF']/float(self.stats['hands'])
        self.stats['pfr'] = self.stats['RaisedPF']/float(self.stats['hands'])
        self.stats['af'] = self.stats['AFNumerator']/float(self.stats['AFDenominator']) if self.stats['AFDenominator'] > 0 else 'Inf'
        self.stats['pfhb'] = self.stats['20RaiseOrCallPF']/float(self.stats['hands'])
        
    def respond(self):
        if DEBUG: print self.hands_played, self.last_hand, self.hand, self.board
        if DEBUG: print self.actions, self.opponent
        self.calculate_ev()
        self.hand_confidence()
        if DEBUG: print "ev=%d, pot=%d, bound=%d" % (self.ev*100, self.pot, self.bound)
        if self.hands_played != self.last_hand and self.hands_played:
            if self.hands_played == self.last_hand + 2: #if we missed one
                self.calculate_stats(self.last[0])
            self.calculate_stats(self.last[1])
            self.last_hand = self.hands_played
            self.bot.new_hand() #notify our bot of new hand
        if DEBUG: print [(x, self.stats[x]) for x in ['vpip', 'pfr', 'af', 'AFNumerator', 'AFDenominator', '20RaiseOrCallPF', 'pfhb']]
        action = self.bot.respond(self)
        #if DEBUG: raw_input()
        return action

class BaseBot(Template):
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        Template.__init__(self)
        # my name
        self.name = "basebot"
        
        self.pfeq = 0   #value between 0 and 4 to indicate what range
                        # our preflop equity was in. 0 = 0-20%, 1=20-40%, etc
        self.my_last_action = {'action':FOLD, 'first':False, 'reraise':False, 'street':PREFLOP, 'betfromaf':False, 'amount':0}


    def parameterize(self, equity):
        #return min(int(equity*100)/20,4)
        ev = equity*100
        if ev < 20:
            return 0
        elif ev < 40:
            return 1
        elif ev < 50:
            return 2
        elif ev < 60:
            return 3
        return 4
        

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
                my_action = Raise(randint(int(LOW*stack_size),int(MID*stack_size))) #low-mid
            elif last_action == RAISE:
                if self.my_last_action['action'] == CHECK or last_act[1].amount/float(stack_size) > LOW: #TODO: this should be pot odds!
                    my_action = Fold()
                else:
                    my_action = Call()
        elif self.pfeq == 2:
            if self.first:
                my_action = Raise(LOW*stack_size)
            elif last_action == CALL:
                my_action = Raise(randint(int(LOW*stack_size),int(MID*stack_size))) #low to mid
            elif last_action == RAISE:
                if self.my_last_action['action'] == CHECK or last_act[1].amount/float(stack_size) > MID:
                    my_action = Fold()
                else:
                    my_action = Call()
        elif self.pfeq == 3:
            if self.first:
                my_action = Raise(LOW*stack_size)
            elif last_action == CALL:
                my_action = Raise(MID*stack_size)
            elif last_action == RAISE:
                if self.my_last_action['action'] == CHECK or last_act[1].amount/float(stack_size) > MID:
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
                    my_action = Raise(MID*stack_size)
            elif last_action == CALL:
                my_action = Raise(LOW*stack_size)
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
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 2:
                if brain.stats['af'] < .5:
                    for action in brain.legal:
                        if isinstance(action,Raise) or isinstance(action,Bet):
                            my_action = action
                            self.my_last_action['betfromaf'] = True
                            break
                elif self.first:
                    my_action = Bet(LOW*stack_size)
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(LOW*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_act = Call()
                        elif last_act[1].amount/float(stack_size) <= HIGH:
                            if brain.stats['pfr'] < .2 : #or brain.stats['cr'] < .4
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
                    my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size))) #low-mid
                elif last_action == BET:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
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
                    my_action = Bet(randint(int(MID*stack_size),int(HIGH*stack_size))) #mid_high
                elif last_action == CHECK:
                    my_action = Bet(int(LOW*stack_size))
                elif last_action == BET:
                    my_action = Raise(int(MID*stack_size))
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(int(MID*stack_size))
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
                        my_action = Bet(randint(self.min_bet,int(LOW*stack_size)))
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action in [BET, RAISE]:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 2:
                if brain.stats['af'] < .5:
                    for action in brain.legal:
                        if isinstance(action,Raise) or isinstance(action,Bet):
                            my_action = action
                            self.my_last_action['betfromaf'] = True
                            break
                elif self.first:
                    my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size)))
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(LOW*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_act = Call()
                        elif last_act[1].amount/float(stack_size) <= HIGH:
                            if brain.stats['pfr'] < .2 : #or brain.stats['cr'] < .4
                                my_action = Fold()
                            else:
                                my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['betfromaf']:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_act = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 3:
                if self.first or last_action == CHECK:
                    my_action = Bet(int(MID*stack_size))
                elif last_action == BET:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_action = Raise(int(MID*stack_size))
                        elif last_act[1].amount/float(stack_size) <= HIGH:
                            my_action = Call()
                        else:
                            my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
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
                    my_action = Bet(randint(int(MID*stack_size),int(HIGH*stack_size))) #mid_high
                elif last_action == CHECK:
                    my_action = Bet(int(LOW*stack_size))
                elif last_action == BET:
                    my_action = Raise(int(MID*stack_size))
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(int(MID*stack_size))
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
        elif self.pfeq == 2:
            if eq == 0:
                if self.first:
                    if brain.stats['af'] < .5:
                        my_action = Bet(int(MID*stack_size))
                    else:
                        my_action = Check()
                elif last_action == CHECK:
                    my_action = Bet(MID*stack_size)
                elif last_action in [BET, RAISE]:
                    my_action = Fold()
            elif eq == 1:
                if self.first:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(randint(self.min_bet,int(LOW*stack_size)))
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 2:
                if self.first:
                    if brain.stats['af'] < .5:
                        my_action = Bet(int(MID*stack_size))
                        self.my_last_action['betfromaf'] = True
                    else:
                        my_action = Check()
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 3:
                if self.first or last_action == Check:
                    my_action = Bet(int(MID*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Raise(int(MID*stack_size))
                    elif last_act[1].amount/float(stack_size) <= HIGH:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= HIGH:
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
                    my_action = Bet(randint(int(MID*stack_size),int(HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(int(MID*stack_size))
                elif last_action == BET:
                    my_action = Raise(int(MID*stack_size))
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
                    else:
                        my_action = Raise(int(MID*stack_size))
        elif self.pfeq == 3:
            if eq == 0:
                if self.first:
                    if brain.stats['af'] < .5:
                        my_action = Bet(int(MID*stack_size))
                    else:
                        my_action = Check()
                elif last_action == CHECK:
                    my_action = Bet(int(MID*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
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
                        my_action = Bet(randint(self.min_bet,int(LOW*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(int(LOW*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 2:
                if self.first:
                    if brain.stats['af'] < .5:
                        my_action = Bet(int(MID*stack_size))
                        self.my_last_action['betfromaf'] = True
                    else:
                        my_action = Bet(int(LOW*stack_size))
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 3:
                if self.first or last_action == Check:
                    my_action = Bet(int(MID*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Raise(int(MID*stack_size))
                    elif last_act[1].amount/float(stack_size) <= HIGH:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Raise(self.min_bet)
                        elif last_act[1].amount/float(stack_size) <= HIGH:
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
                    my_action = Bet(int(LOW*stack_size))
                elif last_action == BET:
                    my_action = Call()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(int(MID*stack_size))
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
                    my_action = Bet(int(MID*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
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
                    my_action = Bet(int(MID*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Raise(int(MID*stack_size))
                    elif last_act[1].amount/float(stack_size) <= HIGH:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Raise(self.min_bet)
                            self.my_last_action['reraise'] = True
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['reraise']:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Call()
            elif eq == 3:
                if self.first:
                    my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(int(MID*stack_size))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Raise(2*self.min_bet)
                    elif last_act[1].amount/float(stack_size) <= HIGH:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= HIGH:
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
                    my_action = Bet(randint(int(MID*stack_size),int(HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(int(LOW*stack_size))
                elif last_action == BET:
                    my_action = Raise(int(MID*stack_size))
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(int(MID*stack_size))
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
                        my_action = Bet(MID*stack_size)
                elif last_action == RAISE:
                    my_action = Fold()
            elif eq == 1:
                if brain.stats['af'] < .5:
                    for action in brain.legal:
                        if isinstance(action,Raise):
                            my_action = Raise(MID*stack_size)
                            self.my_last_action['betfromaf'] = True
                            break
                        elif isinstance(action,Bet):
                            my_action = Bet(MID*stack_size)
                            self.my_last_action['betfromaf'] = True
                            break
                elif self.first:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(randint(self.min_bet,int(LOW*stack_size)))
                elif last_action == CHECK:
                        my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size)))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
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
                if brain.stats['af'] < .5:
                    for action in brain.legal:
                        if isinstance(action,Raise):
                            my_action = Raise(MID*stack_size)
                            self.my_last_action['betfromaf'] = True
                            break
                        elif isinstance(action,Bet):
                            my_action = Bet(MID*stack_size)
                            self.my_last_action['betfromaf'] = True
                            break
                elif self.first:
                    my_action = Bet(LOW*stack_size)
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(LOW*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    elif last_act[1].amount/float(stack_size) <= MID:
                        if brain.stats['af'] > 1.5:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_action = Call()
                        elif last_act[1].amount/float(stack_size) <= MID:
                            if brain.stats['pfr'] < .2 : #or brain.stats['cr'] < .4 or this is a continutation bet
                                my_action = Fold()
                            else:
                                my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['betfromaf']:
                        my_action = Fold()
            elif eq == 3:
                if self.first or last_action == CHECK:
                    my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size)))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if brain.stats['af'] < .5:
                            my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= MID:
                                my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        #if opp never bet/raised: fold
                        my_action = Call()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(MID*stack_size),int(HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(LOW*stack_size)
                elif last_action == BET:
                    my_action = Bet(MID*stack_size)
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(MID*stack_size)
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
                        my_action = Bet(MID*stack_size)
                elif last_action == RAISE:
                    my_action = Fold()
            elif eq == 1:
                if self.first:
                    if brain.stats['af'] < .5:
                        for action in brain.legal:
                            if isinstance(action,Raise):
                                my_action = Raise(MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                            elif isinstance(action,Bet):
                                my_action = Bet(MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                    else:
                        if randint(0,99) < 50:
                            my_action = Check()
                        else:
                            my_action = Bet(randint(self.min_bet,int(LOW*stack_size)))
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 2:
                if self.first:
                    if brain.stats['af'] < .5:
                        for action in brain.legal:
                            if isinstance(action,Raise):
                                my_action = Raise(MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                            elif isinstance(action,Bet):
                                my_action = Bet(MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                    else:
                        my_action = Bet(LOW*stack_size)
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(LOW*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    elif last_act[1].amount/float(stack_size) <= MID:
                        if brain.stats['af'] > 1.5:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if self.my_last_action['betfromaf']:
                            if last_act[1].amount/float(stack_size) <= MID:
                                my_action = Call()
                            else:
                                my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= LOW:
                                my_action = Call()
                            elif last_act[1].amount/float(stack_size) <= HIGH:
                                if brain.stats['pfr'] < .2 : #or brain.stats['cr'] < .4 or this is a continutation bet
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
                    my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size)))
                elif last_action == CHECK:
                    if stack_size > 1.7*400:
                        my_action = Bet(stack_size)
                    else:
                        my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size)))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Call()
                    elif last_act[1].amount/float(stack_size) <= HIGH:
                        if randint(0,99) < 50:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if brain.stats['af'] < .5:
                            my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= MID:
                                my_action = Call()
                            else:
                                my_action = Fold()
                    else:
                        #if opp has not raised/bet this hand: fold
                        my_action = Call()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(MID*stack_size),int(HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(LOW*stack_size)
                elif last_action == BET:
                    my_action = Raise(MID*stack_size)
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(MID*stack_size)
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
        elif self.pfeq == 2:
            if eq == 0:
                if self.first:
                    my_action = Check()
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Bet(MID*stack_size)
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
                    if brain.stats['af'] < .5:
                        for action in brain.legal:
                            if isinstance(action,Raise):
                                my_action = Raise(MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                            elif isinstance(action,Bet):
                                my_action = Bet(MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                    else:
                        if randint(0,99) < 50:
                            my_action = Check()
                        else:
                            my_action = Bet(randint(self.min_bet,int(LOW*stack_size)))
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    elif last_act[1].amount/float(stack_size) <= MID:
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
                            if last_act[1].amount/float(stack_size) <= LOW:
                                my_action = Call()
                            else:
                                my_action = Fold()
            elif eq == 2:
                if self.first:
                    my_action = Bet(MID*stack_size)
                elif last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    elif last_act[1].amount/float(stack_size) <= MID:
                        if brain.stats['af'] > 1.5:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_action = Call()
                        elif last_act[1].amount/float(stack_size) <= HIGH:
                            if brain.stats['pfr'] < .2 : #or brain.stats['cr'] < .4 or this is a continutation bet
                                my_action = Fold()
                            else:
                                my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 3:
                if self.first:
                    my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size)))
                elif last_action == CHECK:
                    if stack_size > 1.7*400:
                        my_action = Bet(stack_size)
                    else:
                        my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size)))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Call()
                    elif last_act[1].amount/float(stack_size) <= HIGH:
                        if randint(0,99) < 50:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if brain.stats['af'] < .5:
                            my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= MID:
                                my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        #if opp has not raised/bet this hand: fold
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(MID*stack_size),int(HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(LOW*stack_size)
                elif last_action == BET:
                    my_action = Raise(MID*stack_size)
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(MID*stack_size)
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
        elif self.pfeq == 3:
            if eq == 0:
                if self.first:
                    my_action = Bet(MID*stack_size)
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Bet(MID*stack_size)
                    else:
                        my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount == 2*self.my_last_action['amount']:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        my_action = Fold()
            elif eq == 1:
                if self.first:
                    if brain.stats['af'] < .5:
                        for action in brain.legal:
                            if isinstance(action,Raise):
                                my_action = Raise(MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                            elif isinstance(action,Bet):
                                my_action = Bet(MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                    else:
                        if randint(0,99) < 50:
                            my_action = Check()
                        else:
                            my_action = Bet(LOW*stack_size)
                elif last_action == CHECK:
                    my_action = Bet(MID*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if self.my_last_action['betfromaf']:
                            my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= LOW:
                                my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 2:
                if self.first:
                    if stack_size <= .6 * 400:
                        my_action = Check()
                    else:
                        my_action = Bet(MID*stack_size)
                elif last_action == CHECK:
                    my_action = Bet(MID*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Raise(MID*stack_size)
                    elif last_act[1].amount/float(stack_size) <= MID:
                        if brain.stats['af'] < .5:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_action = Call()
                        elif last_act[1].amount/float(stack_size) <= HIGH:
                            if brain.stats['pfr'] < .2 : #or brain.stats['cr'] < .4 or this is a continutation bet
                                my_action = Fold()
                            else:
                                my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_action = Call()
                        elif last_act[1].amount/float(stack_size) <= MID:
                            if stack_size <= .6 * 400:
                                my_action = Fold()
                            else:
                                my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 3:
                if self.first:
                    my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size)))
                elif last_action == CHECK:
                    if stack_size > 1.7*400:
                        my_action = Bet(stack_size)
                    else:
                        my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size)))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Raise(HIGH*stack_size)
                    elif last_act[1].amount/float(stack_size) <= HIGH:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                            if last_act[1].amount/float(stack_size) <= MID:
                                my_action = Call()
                            elif last_act[1].amount/float(stack_size) <= HIGH:
                                if brain.stats['af'] < .5:
                                    my_action = Fold()
                                else:
                                    my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        #if opp has not raised/bet this hand: fold
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == RAISE:    
                        my_action = Call()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(MID*stack_size),int(HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(LOW*stack_size)
                elif last_action == BET:
                    my_action = Raise(MID*stack_size)
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        else:
                            my_action = Raise(stack_size)
                    elif self.my_last_action['action'] == BET:
                        my_action = Raise(MID*stack_size)
                    elif self.my_last_action['action'] == RAISE:
                        my_action = Raise(stack_size)
        elif self.pfeq == 4:
            if eq == 0:
                if self.first or last_action == CHECK:
                    my_action = Check()
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
            elif eq == 1:
                if self.first:
                    if brain.stats['af'] < .5:
                        for action in brain.legal:
                            if isinstance(action,Raise):
                                my_action = Raise(MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                            elif isinstance(action,Bet):
                                my_action = Bet(MID*stack_size)
                                self.my_last_action['betfromaf'] = True
                                break
                    else:
                        if randint(0,99) < 50:
                            my_action = Check()
                        else:
                            my_action = Bet(randint(int(self.min_bet),int(LOW*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size)))
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if self.my_last_action['betfromaf']:
                            my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= LOW:
                                my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 2:
                if self.first:
                    my_action = Bet(MID*stack_size)
                    if brain.stats['af'] < .5:
                        self.my_last_action['betfromaf'] = True
                elif last_action == CHECK:
                    if randint(0,99) < 50:
                        my_action = Check()
                    else:
                        my_action = Bet(MID*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= MID:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if self.my_last_action['betfromaf']:
                            if last_act[1].amount/float(stack_size) <= MID:
                                my_action = Call()
                            else:
                                my_action = Fold()
                        else:
                            if last_act[1].amount/float(stack_size) <= MID:
                                my_action = Call()
                            elif last_act[1].amount/float(stack_size) <= HIGH:
                                if brain.stats['af'] < .5:
                                    my_action = Fold()
                                else:
                                    my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= LOW:
                            my_action = Call()
                        else:
                            my_action = Fold()
            elif eq == 3:
                if self.first:
                    my_action = Bet(randint(int(LOW*stack_size),int(MID*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(MID*stack_size)
                elif last_action == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_action = Raise(LOW*stack_size)
                    elif last_act[1].amount/float(stack_size) <= HIGH:
                        my_action = Call()
                    else:
                        my_action = Fold()
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                            if brain.stats['af'] < .5:
                                my_action = Fold()
                            elif last_act[1].amount/float(stack_size) <= MID:
                                my_action = Call()
                            else:
                                my_action = Fold()
                    elif self.my_last_action['action'] == BET:
                        if last_act[1].amount/float(stack_size) <= HIGH:
                            my_action = Call()
                        else:
                            my_action = Fold()
                    elif self.my_last_action['action'] == RAISE:    
                        my_action = Call()
            elif eq == 4:
                if self.first:
                    my_action = Bet(randint(int(MID*stack_size),int(HIGH*stack_size)))
                elif last_action == CHECK:
                    my_action = Bet(MID*stack_size)
                elif last_action == BET:
                    my_action = Raise(MID*stack_size)
                elif last_action == RAISE:
                    if self.my_last_action['first']:
                        if last_act[1].amount/float(stack_size) <= MID:
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
                my_action = Bet(MID*stack_size)
            elif last_action == BET:
                if last_act[1].amount/float(stack_size) <= MID:
                    my_action = Call()
                elif last_act[1].amount/float(stack_size) <= HIGH:
                    if brain.stats['af'] > 1.5:
                        my_action = Call()
                    else:
                        my_action = Fold()
                else:
                    my_action = Fold()
            elif last_action == RAISE:
                if self.my_last_action['action'] == BET:
                    if last_act[1].amount/float(stack_size) <= LOW:
                        my_act = Call()
                    elif last_act[1].amount/float(stack_size) <= HIGH:
                        if brain.stats['pfr'] < .2 : #or brain.stats['cr'] < .4 or cb
                            my_action = Fold()
                        else:
                            my_action = Call()
                    else:
                        my_action = Fold()
        elif eq == 3:
            if self.first or last_action == CHECK:
                my_action = Bet(MID*stack_size)
            elif last_action == BET:
                if last_act[1].amount/float(stack_size) <= MID:
                    my_action = Raise(MID*stack_size)
                elif last_act[1].amount/float(stack_size) <= HIGH:
                    #if opp never raised b4: fold
                    my_action = Call()
                else:
                    my_action = Fold()
            elif last_action == RAISE:
                if self.my_last_action['first']:
                    if brain.stats['af'] < .5:
                        my_action = Fold()
                    else:
                        if last_act[1].amount/float(stack_size) <= MID:
                            my_action = Call()
                        elif last_act[1].amount/float(stack_size) <= HIGH:
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
                        my_action = Bet(HIGH*stack_size)
                    else:
                        my_action = Bet(MID*stack_size)
            elif last_action == CHECK:
                my_action = Bet(MID*stack_size)
            elif last_action == BET:
                my_action = Raise(MID*stack_size)
            elif last_action == RAISE:
                my_action = Raise(stack_size)
        return my_action

