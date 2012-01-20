from pokerbots.player.ourbot import TheBostonDerby
from pokerbots.player.ODoyleBot import odoylebot
from pokerbots.player.RockyBot2 import rockybot2
from pokerbots.player.LukeBotAgg import lukebotagg
from pokerbots.player.MLKBot import mlkbot
from pokerbots.player.ManBearPig import manbearpigbot
from pokerbots.player.SouthStationBot import southstation
from pokerbots.player.LukeBot import LukeBot

class MasterBates(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "MasterBates"
        self.bot = lukebotagg()
        self.high_chip_bot = odoylebot()
        self.low_chip_bot = rockybot2()

class MasterBates1(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "MasterBates1"
        self.bot = manbearpigbot()
        self.high_chip_bot = odoylebot()
        self.high_chip_bot.eq_ranges = [[10, 10, 40, 65], [5, 30, 60, 60], [10, 10, 45, 90], [15, 50, 70, 95]]
        self.low_chip_bot = rockybot2()

class MasterBates2(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "MasterBates2"
        self.bot = mlkbot()
        self.high_chip_bot = odoylebot()
        self.low_chip_bot = rockybot2()

class MasterBates3(TheBostonDerby):
    def __init__(self):
        TheBostonDerby.__init__(self)
        self.name = "MasterBates3"
        self.bot = LukeBot()
        self.bot.eq_ranges = [[23, 61, 72, 91]]*4
        self.high_chip_bot = odoylebot()
        self.low_chip_bot = rockybot2()


