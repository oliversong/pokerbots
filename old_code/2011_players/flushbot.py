from pokerbots.engine.game import Raise, Check, Call, Bet, Fold
from random import randint

class Flushbot:
    def __init__(self):
        """This is a very simple player that demonstrates the API and is a good
        template for getting started
        """
        # my name
        self.name = "flushbot"

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
        if self.hand[0].get_suit() != self.hand[1].get_suit():
            for action in self.legal:
                if isinstance(action, Check):
                    return action
            return Fold()
        if not self.board.flop(): 
            for action in self.legal:
                if isinstance(action, Raise): #and randint(0, 100) < 30:
                    return action
        elif not self.board.turn():
            if sum([c.get_suit() == self.hand[0].get_suit() for c in self.board.flop()]) > 1:
                for action in self.legal:
                    if isinstance(action, Raise): #and randint(0, 100) < 30:
                        return action
                for action in self.legal:
                    if isinstance(action, Bet): #and randint(0, 100) < 30:
                        return action
                #print "can't bet and can't raise??"
            else:
                for action in self.legal:
                    if isinstance(action, Check):
                        return action
                return Fold()
        elif not self.board.river():
            if sum([c.get_suit() == self.hand[0].get_suit() for c in self.board.flop()]) > 1:
                for action in self.legal:
                    if isinstance(action, Raise): #and randint(0, 100) < 30:
                        return action
                for action in self.legal:
                    if isinstance(action, Bet): #and randint(0, 100) < 30:
                        return action
                #print "can't bet and can't raise??"
            else:
                for action in self.legal:
                    if isinstance(action, Call):
                        return action
                return Check()
        else:
            if sum([c.get_suit() == self.hand[0].get_suit() for c in self.board.flop()]) > 2:
                for action in self.legal:
                    if isinstance(action, Raise): #and randint(0, 100) < 30:
                        return action
                for action in self.legal:
                    if isinstance(action, Bet): #and randint(0, 100) < 30:
                        return action
                #print "can't bet and can't raise??"
            else:
                for action in self.legal:
                    if isinstance(action, Call):
                        return action
                return Check()
        for action in self.legal:
            if isinstance(action, Call):
                return action
        return Check()

