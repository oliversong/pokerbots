from pokerbots.player.ourbot import TheBostonDerby
from pokerbots.player.ODoyleBot import odoylebot
from pokerbots.player.RockyBot2 import rockybot2
from pokerbots.player.LukeBotAgg import lukebotagg
from pokerbots.player.MLKBot2 import mlkbot2
from pokerbots.player.ManBearPig import manbearpigbot
from pokerbots.player.SouthStationBot import southstation
from pokerbots.player.LukeBot import LukeBot
from pokerbots.player.TheBostonDerbyA import thebostonderbya


class MashupBot(TheBostonDerby):
    def __init__(self):
        self.bots = [manbearpigbot(),lukebotagg(),thebostonderbya(),mlkbot2(),rockybot2()]
        TheBostonDerby.__init__(self)
        self.name = "MashupBot"

'''
[('ManBearPigBot1', 384),
 ('RockyBot3', 359),
 ('MalcomXBot2', 355),
 ('RockyBot4', 337),
 ('MLKBot2', 336),
 ('MalcomXBot', 333),
 ('RockyBot2', 326),
 ('TheDerbs', 304),
 ('MLKBot2Cool4U', 299),
 ('ManBearPigBot2', 289),
 ('MalcomXBot1', 284),
 ('LukeBotAgg1', 281),
 ('LukeBotAgg3', 271),
 ('LukeBotAgg', 265),
 ('ODoyleBot4', 249),
 ('ManBearPigBot', 239),
 ('LukeBotAgg2', 233),
 ('ODoyleBot5', 211)]
'''

class MashupBot1(TheBostonDerby):
    def __init__(self):
        manbearpigbot1 = manbearpigbot()
        manbearpigbot1.eq_ranges = [[25, 80, 85, 90], [30, 45, 65, 100], [45, 55, 70, 90], [20, 25, 45, 75]]
        mlkbot2cool4u = mlkbot2()
        mlkbot2cool4u.eq_ranges = [[30, 60, 85, 95], [20, 35, 45, 55], [15, 45, 45, 80], [5, 15, 35, 40]]
        lukebotagg3 = lukebotagg()
        lukebotagg3.eq_ranges = [[15, 25, 85, 90], [30, 35, 75, 100], [10, 15, 45, 85], [45, 60, 85, 85]]
        self.bots = [manbearpigbot1,mlkbot2cool4u,lukebotagg3,thebostonderbya()]
        TheBostonDerby.__init__(self)
        self.name = "MashupBot1"

class MashupBot2(TheBostonDerby):
    def __init__(self):
        manbearpigbot1 = manbearpigbot()
        manbearpigbot1.eq_ranges = [[25, 80, 85, 90], [30, 45, 65, 100], [45, 55, 70, 90], [20, 25, 45, 75]]
        rockybot3 = rockybot2()
        rockybot3.eq_ranges = [[5, 50, 85, 90], [45, 60, 65, 80], [5, 10, 65, 80], [10, 55, 75, 100]]
        mlkbot2cool4u = mlkbot2()
        mlkbot2cool4u.eq_ranges = [[30, 60, 85, 95], [20, 35, 45, 55], [15, 45, 45, 80], [5, 15, 35, 40]]
        self.bots = [manbearpigbot1,rockybot3,mlkbot2cool4u,mlkbot2()]
        TheBostonDerby.__init__(self)
        self.name = "MashupBot2"

