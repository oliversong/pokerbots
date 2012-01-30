from MatchHistory import MatchHistory

class PostMatchHistory(MatchHistory):
    def update(self, game):
        self.showStats = {}

        for player in [game.me, game.leftOpp, game.rightOpp]:
            if player.name in self.history.keys():
                self.showStats[player.name] = [[player.holeCard1, player.holeCard2], [0,0]]

        self.computeNewEntries(game)
