from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
from random import randint
import time
from multiprocessing import Process, Queue, cpu_count, Value
import os
for bot in os.listdir('./pokerbots/player/'):
    f = bot.split(".")
    if len(f) == 2 and f[1] == "py" and f[0]:
        exec("from pokerbots.player."+f[0]+" import *")

def playgame(p1, p2):
    t = Table(p1, p2, False)

    t.play_match()
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
    m = 50 #number of games to run for
    
    num_cpus = cpu_count()

    test_bots = [Pokerbot(TheDerbs()),Pokerbot(LukeBotAgg()),Pokerbot(ManBearPigBot()),Pokerbot(MLKBot2()),Pokerbot(ODoyleBot5()),Pokerbot(RockyBot2())]
    score = dict([(bot.name, [0,[0]*len(test_bots)]) for bot in test_bots])
    for i in range(len(test_bots[:-1])):
        start = time.time()
        for j,p2 in enumerate(test_bots):
            if j <= i: continue
            now= time.time()
            p1 = test_bots[i]
            games_to_run = m
            proc = []
            p1_wins = Value('i',0)
            
            print "playing ", p1.name, "vs", p2.name

            for l in range(num_cpus-1):
                p = Process(target=rungames, args=(p1,p2,m/num_cpus,p1_wins))
                proc.append(p)
                p.start()
                games_to_run = games_to_run - m/num_cpus
            
            rungames(p1,p2,m/num_cpus,p1_wins)

            for p in proc:
                p.join()
            score[p1.name][1][j] = p1_wins.value/float(m)
            score[p1.name][0] += p1_wins.value/float(m)
            score[p2.name][1][i] = (m-p1_wins.value)/float(m)
            score[p1.name][0] += (m-p1_wins.value)/float(m)
            print time.time()-start, time.time()-now, '%16s vs. %16s: %d to %d' %(p1.name,p2.name,p1_wins.value,m-p1_wins.value)
        print "finished in", time.time()-start
    ranks = sorted(score.items(),key=lambda x: x[1][0],reverse=True)
    print ranks

