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
        val = [sorted([randint(1,20)*5 for y in range(4)]) for x in range(4)]
        vals.append(val)
    return vals

#{0: [43, 63, 65, 84], 1: [21, 58, 80, 84], 2: [17, 53, 79, 100], 3: [25, 74, 82, 98]}

if __name__ == "__main__":
    upper = 100
    n = 200 #number of individuals
    m = 9#number of games to run for
    
    num_cpus = 1#cpu_count()

    test_bots = [Pokerbot(TheDerbs()),Pokerbot(LukeBotAgg1()),Pokerbot(MalcomXBot()),Pokerbot(ODoyleBot5())]
    #test_bots = [Pokerbot('TheBostonDerby4'),Pokerbot('TheBostonDerby8'),Pokerbot('TheBostonDerby5'),Pokerbot('TheBostonDerby'),Pokerbot('TheBostonDerby6'),Pokerbot('Flopallin')]
    use_lukes = True
    if use_lukes:
        vals = generate_vals()
    else:
        vals = generate_vals_boston()

    bots = []
    for i,genome in enumerate(vals):
        bot = Pokerbot(RockyBot2())
        bot.bot.bot.eq_ranges=genome
        bot.index = i
        bots.append(bot)
    score = [0]*n
    for bot in bots:
        score[bot.index] = [0,[0]*len(test_bots),bot.bot.bot.eq_ranges]
    begin = time.time()
    for i in range(n):
        start = time.time()
        p1 = bots[i]
        print "testing with bot",i,"using gene", p1.bot.bot.eq_ranges
        for j,p2 in enumerate(test_bots):
            now= time.time()
            games_to_run = m
            proc = []
            p1_wins = Value('i',0)#[resultsaccum() for i in range(num_cpus)]

            for l in range(num_cpus-1):
                p = Process(target=rungames, args=(p1,p2,m/num_cpus,p1_wins))
                proc.append(p)
                p.start()
                games_to_run = games_to_run - m/num_cpus
            
            #print games_to_run
            rungames(p1,p2,m/num_cpus,p1_wins)

            for p in proc:
                p.join()
            p2.bot.restart()
            score[p1.index][1][j] = p1_wins.value/float(m)
            score[p1.index][0] += p1_wins.value/float(m)
            #score[p2.bot.eq_ranges] += p2_wins/float(m)
            print i,time.time()-now, score[p1.index][0]/float(j+1),score[p1.index][1]
        print "finished in", time.time()-start
    print "took total time of", time.time()-begin
    ranks = sorted(score,key=lambda x: x[0],reverse=True)
    ranked = sorted(score,key=lambda x: min(x[1]),reverse=True)
    for line in  ["%.2f, " %(x[0]) + str(["%.2f" %(y) for y in x[1]]) + ", " + str(x[2]) for x in ranks[:5]]:
        print line
    print ""
    for line in ["%.2f, " %(x[0]) + str(["%.2f" %(y) for y in x[1]]) + ", " + str(x[2]) for x in ranked[:5]]:
        print line

