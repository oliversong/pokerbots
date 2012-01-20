from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
from random import randint
import time
from multiprocessing import Process, Queue, cpu_count, Value
import os,copy
for bot in os.listdir('./pokerbots/player/'):
    f = bot.split(".")
    if len(f) == 2 and f[1] == "py" and f[0]:
        exec("from pokerbots.player."+f[0]+" import *")

def playgame(p1, p2):
    t = Table(p1, p2)

    t.play_match()
    return t.p2.stack == 0 #return 1 if p1 won, 0 if p2 won

def rungames(num_games,in_q,out_q):
    for p1 in iter(in_q.get, 'STOP'):
        first= True
        scores = [0]*len(test_bots)
        for j,p2 in enumerate(test_bots):
            if isinstance(p1.bot,p2.bot.__class__): continue
            res = 0
            now= time.time()
            stats = {}
            for i in range(num_games):
                res += playgame(p1,p2)
            scores[j] = res
            print "testing bot %d"%(p1.index),"vs %16s using gene" % (p2.name), p1.bot.bot.eq_ranges, "and after %.2f won %.2f" % (time.time()-now, res/float(num_games))
        out_q.put((p1,scores))

def generate_vals_boston():
    vals = []
    for it in range(n):
        val = []
        for i in range(4):
            i = randint(10,upper)
            val.append(i)
        while sorted(val) in vals:
            val = []
            for i in range(4):
                i = randint(10,upper)
                val.append(i)
        vals.append(tuple(sorted(val)))
    return vals
    
def generate_vals():
    vals = []
    for it in range(n):
        val = dict([(x,sorted([randint(1,20)*5 for y in range(4)])) for x in range(4)])
        vals.append(val)
    return vals


if __name__ == "__main__":
    upper = 100
    n = 400 #number of individuals
    m = 10 #number of games to run for
    
    num_cpus = cpu_count()

    test_bots = [Pokerbot(TheDerbs()),Pokerbot(LukeBotAgg()),Pokerbot(ManBearPigBot1()),Pokerbot(MLKBot2()),Pokerbot(ODoyleBot5()),Pokerbot(RockyBot2()),Pokerbot(CheezierBot()),Pokerbot(FlyingSpagBot())]
    use_lukes = True
    if use_lukes:
        vals = generate_vals()
    else:
        vals = generate_vals_boston()
    
    match_queue = Queue()
    result_queue = Queue()

    if 0:
        bots = [Pokerbot(TheDerbs()),Pokerbot(LukeBotAgg()),Pokerbot(ManBearPigBot1()),Pokerbot(MLKBot2()),Pokerbot(ODoyleBot5()),Pokerbot(RockyBot2()),PokerBot(CheezierBot()),PokerBot(FlyingSpagBot())]
        n = len(bots)
        for i,bot in enumerate(bots):
            bot.index = i
    else:
        bots = []
        for i,genome in enumerate(vals):
            bot = Pokerbot(ManBearPigBotNew())
            bot.bot.bot.eq_ranges=genome
            bot.index = i
            bots.append(bot)
    score = [0]*n
    for bot in bots:
        score[bot.index] = [0,[0]*len(test_bots),bot.index,bot.name,bot.bot.bot.eq_ranges]
    statistics = [0]*n

    start = time.time()
    for i in range(n):
        p1 = bots[i]
        match_queue.put(p1)
    
    proc = []
    for l in range(num_cpus):
        p = Process(target=rungames, args=(m,match_queue,result_queue))
        proc.append(p)
        p.start()

    for i in range(n):
        p1,p1_wins = result_queue.get()
        score[p1.index][1] = p1_wins
        score[p1.index][0] = sum(p1_wins)
    
    for l in range(num_cpus):
        match_queue.put('STOP')

    print "finished in", time.time()-start
    ranks = sorted(score,key=lambda x: x[0],reverse=True)
    print ranks[:10]

