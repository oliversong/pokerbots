""" 
pokerbot.py
This is the basic player class that uses an AI as a brain

"""

import copy
import time
import os

from pokerbots.engine.game import Card, Board, Check

class Pokerbot(object):
    """A pokerbot is instantiated with a string that corresponds to the brain
    file. 
    """
    def __init__(self, bot):
        # active, all_in, and seat are internal
        self.active = False
        self.stack = None
        self.all_in = False
        self.hand = None
        self.seat = None
        self.pip = 0
        self.button = None
        
        self.time = 20.0
        if isinstance(bot,str):
            exec('from pokerbots.player.' + bot + '.' + bot + ' import ' + bot + ' as Bot')
            self.bot = Bot()
        else:
            self.bot = bot
        self.name = self.bot.name


    def respond(self, game_state):
        """Maps a state dictionary into variables for a bot to use and then
        queries for a response"""
        # set their hand incase they changed it
        # also their game data: stack, money put in pot, is button
        opp = 1
        if game_state['players'][1]['name'] == self.name:
            opp = 0

        game_state = copy.deepcopy(game_state)

        self.bot.stack = self.stack
        self.bot.hand = (Card(self.hand[0].rank, self.hand[0].suit),
                         Card(self.hand[1].rank, self.hand[1].suit))
        self.bot.pip = self.pip
        self.bot.button = self.button
        self.bot.time = float(self.time)

        self.bot.opponent = {'name': game_state['players'][opp]['name'],
                             'stack': game_state['players'][opp]['stack'],
                             'pip': game_state['players'][opp]['pip'],
                             'button': game_state['players'][opp]['button'],
                             'time': game_state['players'][opp]['time']}

        # game parameters
        self.bot.bb = game_state['bb']
        self.bot.sb = game_state['sb']
        self.bot.hands_played = game_state['hands_played']
        self.bot.board = Board(game_state['board'].cards)
        self.bot.last = game_state['last'][:]
        self.bot.actions = game_state['actions'][:]
        self.bot.legal = game_state['legal'][:]
        self.bot.pot = game_state['pot']
        
        # already out of time
        if self.time <= 0 and not self.bot.unlimited:
            return Check()

        start = time.time()
        response = self.bot.respond()
        end = time.time()
        total = end - start

        self.time -= total

        # over-used their time
        if self.time <= 0 and not self.bot.unlimited:
            return Check()

        return response


    def reset(self, won, last_hand):
        """Calls a reset method in each bot that indicates a match
        has ended"""
        try:
            self.bot.reset(won, last_hand)
        except:
            pass
