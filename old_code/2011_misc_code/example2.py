from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
from multiprocessing import Process, Queue, cpu_count, Value
import os
for bot in os.listdir('./pokerbots/player/'):
    f = bot.split(".")
    if len(f) == 2 and f[1] == "py" and f[0]:
        exec("from pokerbots.player."+f[0]+" import *")

P1 = MasterBates()
P2 = LukeBotAgg()
GAMES = 50

def playgame(p1, p2):
    p1 = Pokerbot(p1)
    p2 = Pokerbot(p2)

    t = Table(p1, p2, False)

    while t.p1.stack > 0 and t.p2.stack > 0:
        t.play()
    return t.p2.stack == 0 #return 1 if p1 won, 0 if p2 won

def rungames(p1,p2,num_games,output):
    res = 0
    for i in range(num_games):
        r = playgame(p1,p2)
        if r: print p1.name + " won",
        else: print p2.name + " won",
        print "game %d" % i
        res += r
    while not output.acquire(): continue
    output.value += res
    output.release()

if __name__ == "__main__":
    num_cpus = cpu_count()
    games_to_run = GAMES
    proc = []
    results = Value('i',0)
    for i in range(num_cpus-1):
        p = Process(target=rungames, args=(P1,P2,GAMES/num_cpus,results))
        proc.append(p)
        p.start()
        games_to_run = games_to_run - GAMES/num_cpus
    
    rungames(P1,P2,games_to_run,results)

    for p in proc:
        p.join()
        
    print "player", P1.name, "won", results.value, 'or',results.value/float(GAMES), "games"
