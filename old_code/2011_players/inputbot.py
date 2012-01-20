from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from pokerbots.player.ourbot import TheBostonDerby
from random import randint

class CustomBot0(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "CustomBot0"
        self.bot = InputBot()

class CustomBot1(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "CustomBot1"
        self.bot = InputBot()

class InputBot:
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        # my name
        self.name = "InputBot"

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

    def respond(self,brain):
        """Based on your game state variables (see the __init__), make a
        decision and return an action. If you return an illegal action, the
        engine will automatically fold you
        """

        print(brain.board)
        print(brain.hand[0])
        print(brain.hand[1])
        print(brain.stack)
        end = len(brain.actions)-1
        print(brain.actions[end-1])
        print(brain.actions[end])
        

        command = raw_input("what action do you want to do:")
        act = command.split()[0]


        if act == "check":
            return Check()
        elif act == "fold":
            return Fold()
        elif act == "raise":
            amt = command.split()[1]
            for action in brain.legal:
                if isinstance(action, Raise):
                    return Raise(int(amt))
                else:
                    return Bet(int(amt))
        elif act == "bet":
            amt = command.split()[1]
            return Bet(int(amt))
        else:
            return Call()
        
        

##        for action in self.legal:
##            if isinstance(action, Raise):
##                if self.hand[0].rank == self.hand[1].rank:
##                    return Raise(self.stack + self.pip)
##                return Call()
##
##        for action in self.legal:
##            if isinstance(action, Bet):
##                if randint(0, 100) < 35:
##                    return Bet(self.stack/2)
##            return Check()
##
##        return Fold()


