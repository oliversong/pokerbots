from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from random import randint

class Pocketpair:
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        # my name
        self.name = "pocketpair"

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

    def respond(self):
        if self.hand[0].get_rank() == self.hand[1].get_rank():
            for action in self.legal:
                if isinstance(action, Raise): #and randint(0, 100) < 30:
                    return action
        else:
            for action in self.legal:
                if isinstance(action, Fold):
                    return action
        for action in self.legal:
            if isinstance(action, Call):
                return action
        return Check()
