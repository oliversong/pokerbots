from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
import time
import os
for bot in os.listdir('./pokerbots/player/'):
    f = bot.split(".")
    if len(f) == 2 and f[1] == "py" and f[0]:
        exec("from pokerbots.player."+f[0]+" import *")

P1 = RockyBot2()
P2 = LukeBotAgg3()
p1 = Pokerbot(P1)
p2 = Pokerbot()
p1_wins = 0
p2_wins = 0
num_matches = 9

for i in range(num_matches):
    t = Table(p1, p2,True)
    start = time.time()
    t.play_match()
    print time.time()-start,
    if t.p1.stack == 0:
        print t.p2.name, "won",
        p2_wins += 1
    else:
        print t.p1.name, "won",
        p1_wins += 1
    print "game %d" %i

print t.p1.name, "won", p1_wins, "times"
print t.p2.name, "won", p2_wins, "times"
