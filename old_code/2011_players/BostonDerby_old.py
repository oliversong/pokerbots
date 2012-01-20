CHECK, BET, RAISE, FOLD, CALL, DEAL, SHOW, WON, POST = range(9)
PREFLOP, FLOP, TURN, RIVER = range(4)
DEBUG = False

from pokerbots.engine.game import Raise, Check, Call, Bet, Fold, Deal, Show, Won, Post
from pokerbots.player.basebot import BaseBot
from random import randint
from collections import deque
from pokerbots.player.pocketlookup import lookuphand,lookupvalue
from pokereval import PokerEval

class TheBostonDerbyOld:
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        # my name
        self.name = "theBostonDerby"

        self.reset(False,[])
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
        self.LOW = .02
        self.MID = .08
        self.HIGH = .15

    def reset(self, won, last_hand):
        """Reset accepts a boolean indicating whether you won a match and
        provides the last hand if you want to update any statistics from it
        """
        self.my_stats = {   'hands':0,
                            '^VPIP':[0,0,0,0],
                            'VPIP':[0,0,0,0],  # amount voluntarily placed in pot
                            '^INCR':[0,0,0,0],
                            'INCR':[0,0,0,0],   # frequency of raises
                            '^AF':0,
                            '_AF':0,
                            'AF':0,    # aggression frequency = (bets + raises)/(checks + calls)
                            #pre flop
                            '^ST':0,
                            'ST':0,    # steals = how often he raises when has first action
                            '^LMP':0,
                            'LMP':0,  # how often opponent calls
                            '_3B':0,
                            '^FBB':0,
                            'FBB':0,    # how often, after small blind raises, big blind folds
                            '^3B':0,
                            '3B':0,    # how often, after small blind raises, big blind raises
                            '_4B':0,
                            '^F3B':0,
                            'F3B':0,   # how often, after small blind raises and then big blind raises, small blind folds
                            '^4B':0,
                            '4B':0,    # how often, the small bind raises in above circumstances
                            '_F4B':0,
                            '^F4B':0,
                            'F4B':0,    #how often big blind folds to 4B
                            #flop
                            '_COB':0,
                            '^COB':0,
                            'COB':0,    # continuation bet = how often betting after betting/raising on preflop
                            '_FCOB':0,
                            '^FCOB':0,
                            'FCOB':0,   # how often opp folds to a continuation bet
                            #turn
                            '_2COB':0,
                            '^2COB':0,
                            '2COB':0,   # how often opp cb twice, once on flop and once on turn
                            '_F2COB':0,
                            '^F2COB':0,
                            'F2COB':0,  # how often opp folds to 2nd continuation bet.
                            '_CHBR':[0,0,0,0],
                            '^CHBR':[0,0,0,0],
                            'CHBR':[0,0,0,0],    # how often opp check raises
                         }
                     
        self.opp_stats = self.my_stats.copy()
        self.opp_stats['^VPIP'] = [0,0,0,0]
        self.opp_stats['VPIP'] = [0,0,0,0]
        self.opp_stats['^INCR'] = [0,0,0,0]
        self.opp_stats['INCR'] = [0,0,0,0]
        self.opp_stats['_CHBR'] = [0,0,0,0]
        self.opp_stats['^CHBR'] = [0,0,0,0]
        self.opp_stats['CHBR'] = [0,0,0,0]
        self.last = None
        self.opp_hand = 100.0
        self.cory_stats = {'A':0, 'W':0, 'C':0}

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
            my_hand = [self.card2str(c) for c in self.hand]
            dead = my_hand
            if self.board.river():
                board += [self.card2str(self.board.turn()), self.card2str(self.board.river())]
                dead += board[:]
            elif self.board.turn():
                board += [self.card2str(self.board.turn()), '__']
                dead += board[:-1]
            else:
                board += ['__','__']
                dead += board[:-2]
            if self.opp_hand == 100.0:
                ev = self.ev_calc.poker_eval(game="holdem",pockets=[[self.card2str(c) for c in self.hand],['__','__']],dead=[],board=board,iterations=1000)
                ev = ev['eval'][0]['ev']/10.0
            else:
                hands = reduce(lambda x,y:x+y, lookupvalue[:int(self.opp_hand*10)])
                wins = 0
                iters = 30
                num_hands = 0
                for hand in hands:
                    if hand[0] in dead or hand[1] in dead: continue
                    ev = self.ev_calc.poker_eval(game="holdem",pockets=[my_hand,list(hand)],dead=[],board=board,iterations=iters)
                    wins += ev['eval'][0]['winhi']+ev['eval'][0]['tiehi']/2.0
                    num_hands += 1
                ev = wins/float(num_hands*iters)
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
                if self.ev > .9:# or (self.stats['pfhb'] > 0.25 and self.hands_played > 12):
                    self.bound = stack_size
                elif self.ev > .8:
                    self.bound = int(.1 * stack_size)
                elif self.ev > .5:
                    self.bound = 2 * self.bb
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
        tallies = {'raises':0, 'bets':0, 'folds':0, 'calls':0, 'checks':0}
        my_actions = dict(zip(range(4),[tallies.copy() for x in range(4)]))
        opp_actions = dict(zip(range(4),[tallies.copy() for x in range(4)]))
        hand = deque(last[:])
        act = hand.popleft() #first action is always sb posting their blind
        my_actions['position'] = act[0] == self.name #position = 1 means sb, 0 means BB
        opp_actions['position'] = not my_actions['position'] #if i'm not small blind, opp must be
        act = hand.pop()
        my_actions['won'] = act[0] == self.name
        opp_actions['won'] = not my_actions['won']
        this_hand = {self.name:my_actions, self.opponent['name']:opp_actions, 'steal':False, 'limp':False}
        hand.popleft() # second action is always bb posting, and is useless

        street = 0 #0 is preflop, 1 is flop, 2 is turn and 3 is river 
        first = True
        while len(hand) > 0 :
            act = hand.popleft()
            if act[0] == 'Dealer': #then this action corresponds to changing street
                street += 1
                continue
            action = self.classify(act[1])
            if first:   
                first = False
                if action == RAISE:
                    this_hand['steal'] = True
                elif action == CALL:
                    this_hand['limp'] = True

            if act[0] in [self.name, self.opponent['name']]:
                if action == RAISE:
                    this_hand[act[0]][street]['raises'] += 1
                elif action == CHECK:
                    this_hand[act[0]][street]['checks'] += 1
                elif action == CALL:
                    this_hand[act[0]][street]['calls'] += 1
                elif action == FOLD:
                    this_hand[act[0]][street]['folds'] += 1
                elif action == BET:
                    this_hand[act[0]][street]['bets'] += 1
            else:
                print "unknown player: ",act[0]

        self.my_stats['hands'] += 1
        self.opp_stats['hands'] += 1

        self.update_stats(self.opp_stats, my_actions, opp_actions, this_hand['steal'], this_hand['limp'])
        self.update_stats(self.my_stats, opp_actions, my_actions, this_hand['steal'], this_hand['limp'])
        
        self.calc_cory(self.cory_stats, my_actions, opp_actions, this_hand['steal'], this_hand['limp'])
        
        if opp_actions['won']:
            hand = last[:]
            act = hand.pop()
            while act[0] != self.opponent['name']:
                act= hand.pop()
            action = self.classify(act[1])
            if action == RAISE:
                self.cory_stats['A'] += 20
            elif action == BET or action == CALL:
                if action.amount == self.opponent['stack']+self.opponent['pip']:
                    self.cory_stats['A'] += 10
                else:   
                    self.cory_stats['C'] += 20
            
    def calc_cory(self, stats, me, opp, steal, limp):
        stats['A'] += 5*sum([opp[x][y] for x in range(4) for y in ['bets', 'raises']])
        stats['A'] += 10*sum([opp[x]['raises']-1 for x in range(4)])
        stats['C'] += 5*sum([opp[x][y] for x in range(4) for y in ['bets', 'raises', 'calls']])
        stats['C'] += 10*sum([opp[x]['calls']>0 for x in range(4) if opp[x]['raises']>0])
        stats['W'] += 5*(limp and opp['position'])
        stats['W'] += 3*(opp[PREFLOP]['folds']>0)
        stats['W'] += 5*(sum([opp[x]['folds'] for x in [FLOP,TURN,RIVER]])>0)
        stats['A'] += 20*sum([1 for x in [FLOP,TURN,RIVER] if opp[x]['checks']>0 and me[x]['bets'] >0 and opp[x]['raises']>0])

    def update_stats(self,stats,me,opp,steal,limp):
        this_hand = {}
        for street in range(4):
            if opp[street]['raises'] or opp[street]['bets'] or opp[street]['calls']:
                stats['^VPIP'][street] += 1
            if opp[street]['raises']:
                stats['^INCR'][street] += 1
            stats['VPIP'][street] = stats['^VPIP'][street]/float(stats['hands'])
            stats['INCR'][street] = stats['^INCR'][street]/float(stats['hands'])
        this_hand['^AF'] = sum([opp[x]['raises'] + opp[x]['bets'] for x in [FLOP, TURN, RIVER]])
        this_hand['_AF'] = sum([opp[x]['calls'] for x in [FLOP, TURN, RIVER]])
        
        #PREFLOP
        this_hand['^ST'] = steal and opp['position']
        this_hand['^LMP']= limp and opp['position']
        this_hand['_3B'] = steal and not opp['position']
        this_hand['^FBB']= this_hand['_3B'] and opp[0]['folds'] and opp[0]['raises'] == 0
        this_hand['^3B'] = this_hand['_3B'] and opp[0]['raises'] > 0
        this_hand['_4B'] = this_hand['^ST'] and me[0]['raises'] > 0
        this_hand['^F3B']= this_hand['_4B'] and opp[0]['folds'] and opp[0]['raises'] == 1
        this_hand['^4B'] = this_hand['_4B'] and opp[0]['raises'] >= 2
        this_hand['_F4B']= this_hand['^3B'] and me[0]['raises'] >= 2
        this_hand['^F4B']= this_hand['_F4B']and opp[0]['folds'] and opp[0]['raises'] == 1
        
        #FLOP
        this_hand['_COB'] = opp['position'] and opp[0]['raises'] > 0 and me[0]['calls']>0 and me[1]['checks']>0
        this_hand['^COB'] = this_hand['_COB'] and opp[1]['bets'] > 0
        this_hand['_FCOB']= not opp['position'] and me[0]['raises']>0 and opp[0]['calls']>0 and opp[1]['checks']>0 and me[1]['bets']>0
        this_hand['^FCOB']= this_hand['_FCOB'] and opp[1]['folds']>0

        #TURN
        this_hand['_2COB'] = this_hand['^COB'] and me[2]['checks']>0
        this_hand['^2COB'] = this_hand['_2COB'] and opp[2]['bets']>0
        this_hand['_F2COB']= this_hand['_FCOB'] and me[2]['bets']>0
        this_hand['^F2COB']= this_hand['_F2COB'] and opp[2]['folds']>0
        
        this_hand['_CHBR'] = [0,0,0,0]
        this_hand['^CHBR'] = [0,0,0,0]
        
        #POSTFLOP
        for street in [FLOP, TURN, RIVER]:
            this_hand['_CHBR'][street] = opp[street]['checks']>0 and me[street]['bets'] >0
            this_hand['^CHBR'][street] = this_hand['_CHBR'][street] and opp[street]['raises']>0
        
        for stat in stats.keys():
            if this_hand.has_key(stat) and isinstance(this_hand[stat],int):
                stats[stat] += this_hand[stat]
        stats['AF'] = stats['^AF']/float(stats['_AF']) if stats['_AF'] else None
        stats['ST'] = stats['^ST']/float(stats['hands'])
        stats['LMP'] = stats['^LMP']/float(stats['hands'])
        stats['FBB'] = stats['^FBB']/float(stats['_3B']) if stats['_3B'] else None
        stats['3B'] = stats['^3B']/float(stats['_3B']) if stats['_3B'] else None
        stats['F3B'] = stats['^F3B']/float(stats['_4B']) if stats['_4B'] else None
        stats['4B'] = stats['^4B']/float(stats['_4B']) if stats['_4B'] else None
        stats['F4B'] = stats['^F4B']/float(stats['_F4B']) if stats['_F4B'] else None
        stats['COB'] = stats['^COB']/float(stats['_COB']) if stats['_COB'] else None
        stats['FCOB'] = stats['^FCOB']/float(stats['_FCOB']) if stats['_FCOB'] else None
        stats['2COB'] = stats['^2COB']/float(stats['_2COB']) if stats['_2COB'] else None
        stats['F2COB'] = stats['^F2COB']/float(stats['_F2COB']) if stats['_F2COB'] else None
        for street in [FLOP, TURN, RIVER]:
            stats['_CHBR'][street] += this_hand['_CHBR'][street]
            stats['^CHBR'][street] += this_hand['^CHBR'][street]
            stats['CHBR'][street] = stats['^CHBR'][street]/float(stats['_CHBR'][street]) if stats['_CHBR'][street] else None

    def respond(self):
        if DEBUG: print self.name
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
            if DEBUG: print self.opp_stats
            if DEBUG: raw_input()
        if self.board.flop():
            last_act = self.actions[-1]
            last_action = self.classify(last_act[1])
            if last_action == BET:
                if last_act[1].amount < .5*self.pot:
                    self.cory_stats['W'] += 5
                elif last_act[1].amount > self.pot:
                    self.cory_stats['A'] += 10
                if self.button: #he's BB
                    self.cory_stats['A'] += 5
        action = self.bot.respond(self)
        return action

class TheBostonDerby0(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby0"
        self.bot.eq_ranges = (53, 68, 75, 84)

class TheBostonDerby1(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby1"
        self.bot.eq_ranges = (15, 78, 95, 99)

class TheBostonDerby2(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby2"
        self.bot.eq_ranges = (37, 76, 97, 99)

class TheBostonDerby3(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby3"
        self.bot.eq_ranges = (23, 28, 82, 91)

class TheBostonDerby4(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby4"
        self.bot.eq_ranges = (18, 29, 58, 79)

class TheBostonDerby4Copy(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby4Copy"
        self.bot.eq_ranges = (18, 29, 58, 79)

class TheBostonDerby5(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby5"
        self.bot.eq_ranges = (17, 48, 56, 68)

class TheBostonDerby5Copy(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby5"
        self.bot.eq_ranges = (17, 48, 56, 68)

class TheBostonDerby6(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby6"
        self.bot.eq_ranges = (13, 14, 30, 82)

class TheBostonDerby6Copy(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby6Copy"
        self.bot.eq_ranges = (13, 14, 30, 82)

class TheBostonDerby7(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby7"
        self.bot.eq_ranges = (38, 68, 87, 88)
        
class TheBostonDerby8(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby8"
        self.bot.eq_ranges = (10, 62, 63, 80)

class TheBostonDerby8Copy(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby8Copy"
        self.bot.eq_ranges = (10, 62, 63, 80)

class TheBostonDerby9(TheBostonDerbyOld):
    def __init__(self):
        TheBostonDerbyOld.__init__(self)
        self.name = "TheBostonDerby9"
        self.bot.eq_ranges = (15, 29, 33, 50)
