from pokerbots.engine.game import Raise, Check, Call, Bet, Fold, Deal, Show, Won
from random import randint

CHECK, BET, RAISE, FOLD, CALL, DEAL, SHOW, WON = range(8)
PREFLOP, FLOP, TURN, RIVER = range(4)

class Tallybot:
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        # my name
        self.name = "tallybot"

        self.stats = {'hands':0, # number hands played
                      'vpip':0,  # amount voluntarily placed in pot
                      'pfr':0,   # frequency of pre flop raises
                      'actions':{'bets':0,'calls':0,'calls':0,'checks':0,'folds':0},
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
                      'f2cb':0   # how often opp folds to 2nd continuation bet.
                     }
                     
        #perhaps also keep track of all ins? should be related to af...

        # game state variables -- these are updated by the engine which
        # own internal representation. so if you modify them, they'll just
        # be reset. we recommend leaving their init as is
        self.hand = None
        self.last_hand = None
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

    def get_stats(self):
        if self.hands_played != self.last_hand:
            self.stats['hands'] += 1
        actions = self.actions[:]
        last_action = actions.pop()
        our_action = False
        if last_action[0] == 'Dealer':
            our_action = True
            last_action = actions.pop()
        if last_action[0] == self.name: #then we had last action, nothing more to do here
            print "we had last action, returning!"
            return
        if isinstance(last_action[1], Post): return #posting blind is uninteresting action
        if isinstance(last_action[1], Check): 
            action = CHECK
            self.stats['actions']['checks'] += 1
        elif isinstance(last_action[1], Bet):
            action = BET
            self.stats['actions']['bets'] += 1
        elif isinstance(last_action[1], Raise): 
            action = RAISE
            self.stats['actions']['raises'] += 1
        elif isinstance(last_action[1], Fold): 
            action = FOLD
            self.stats['actions']['folds'] += 1
        elif isinstance(last_action[1], Call): 
            action = CALL
            self.stats['actions']['calls'] += 1
            self.stats['limp'] += 1
        else :
            print "umm, unknown action taken!"
            return
        
        if not self.board.flop() or (self.board.flop() and our_action): #preflop action
            if action == BET:
                self.stats['st'] += 1
                self.stats['pfr'] += 1
            elif action == RAISE:
                self.stats['pfr'] += 1
                if isinstance(actions.pop()[1],Raise):
                    if not self.opponent['button']: #if we just raised, and they're big blind, this is 3bet
                        self.stats['3b'] += 1
                    elif isinstance(actions.pop()[1],Raise): #if they're small blind and they raised before we did, then this is 4bet
                        self.stats['4b'] += 1
            elif action == FOLD:
                4/0.0 #will never see fold action?
        elif not self.board.turn() or (self.board.turn() and our_action): #flop
            if action == BET or action == RAISE: #might be a continuation bet
                old_action = actions.pop()
                seen_flop = False
                while old_action[0] != self.opponent['name']:
                    if old_action[0] == 'Dealer' and old_action[1] == 'Flop':
                        seen_flop = True
                    old_action = actions.pop()
                if seen_flop and isinstance(old_action[1],Raise): #raised preflop, this is a continuation bet
                    4/0.0
        elif not self.board.river() or (self.board.river() and our_action): #turn
            3/0.0
        else: #river
            4/0.0

    def classify(self, act):
        action = None
        if isinstance(act[1], Post):
            action = POST
        if isinstance(act[1], Check): 
            action = CHECK
        elif isinstance(act[1], Bet):
            action = BET
        elif isinstance(act[1], Raise): 
            action = RAISE
        elif isinstance(act[1], Fold): 
            action = FOLD
        elif isinstance(act[1], Call): 
            action = CALL
        elif isinstance(act[1], Show):
            action = SHOW
        elif isinstance(act[1], Deal): 
            action = DEAL
        elif isinstance(act[1], Won): 
            action = WON
        else :
            print "umm, unknown action taken!"
        return action
        

    def calculate_stats(self):
        #preflop = {self.name: [], self.opponent['name']: []}
        #parse all actions in previous hand into useful information
        
        tallies = {'raises':0, 'bets':0, 'folds':0, 'calls':0, 'checks':0, 'first':False}
        my_actions = dict(zip(range(4),[tallies.copy() for x in range(4)]))
        opp_actions = dict(zip(range(4),[tallies.copy() for x in range(4)]))
        hand = self.last[:]
        act = hand.pop() #first action is always sb posting their blind
        my_actions['sb'] = act[0] == self.name
        opp_actions['sb'] = not my_actions['sb'] #if i'm not big blind, opp must be
        hand.pop() # second action is always bb posting, and is useless

        if 0:
                    raised[1] += 1 #increment raise count for opponent
                    self.stats['st'] += 1
                    self.stats['pfr'] += 1
                    #if raised[0] == 1: #if we've raised
                    #    if raised[1] == 1: #if this is their first raise
                            
                    if isinstance(actions.pop()[1],Raise):
                        if not self.opponent['button']: #if we just raised, and they're big blind, this is 3bet
                            self.stats['3b'] += 1
                        elif isinstance(actions.pop()[1],Raise): #if they're small blind and they raised before we did, then this is 4bet
                            self.stats['4b'] += 1
        street = 0 #0 is preflop, 1 is flop, 2 is turn and 3 is river    
        first = True
        while len(hand) > 0 :
            act = hand.pop()
            if act[0] != 'Dealer': #then this action corresponds to changing street
                street += 1
                first = True
                continue
            action = self.classify(act)
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
            elif act[0] == self.opponent['name']:
                if action == RAISE:
                    opp_actions[street]['raises'] += 1
                elif action == CHECK:
                    opp_actions[street]['checks'] += 1
                elif action == CALL:
                    opp_actions[street]['calls'] += 1
                elif action == FOLD:
                    opp_actions[street]['folds'] += 1
            else:
                print "unknown player: ",act[0]

        #update relevant statistics
        if self.hands_played != self.last_hand:
            self.stats['hands'] += 1
            self.last_hand = self.hands_played
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
        self.stats['af'] = self.stats['AFNumerator']/float(self.stats['AFDenominator'])
        
    def respond(self):
        #self.get_stats()
        for action in self.legal:
            if isinstance(action, Call):
                return Call()
        return Check()
