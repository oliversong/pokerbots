from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
from random import randint
import time
from multiprocessing.sharedctypes import synchronized
from multiprocessing import Process, Queue, cpu_count, Value, Manager
import os, copy,random
for bot in os.listdir('./pokerbots/player/'):
    f = bot.split(".")
    if len(f) == 2 and f[1] == "py" and f[0]:
        exec("from pokerbots.player."+f[0]+" import *")

def playgame(p1, p2):
    t = Table(p1, p2)
    t.play_match()
    return t.p2.stack == 0 #return 1 if p1 won, 0 if p2 won

def rungames(my_id,num_games,in_q,out_q):
    for p1,p2 in iter(in_q.get, 'STOP'):
        if isinstance(p1.bot,p2.bot.__class__): continue
        if not p1._lock._callmethod('acquire',(False,)):
            in_q.put((p1,p2))
            try:
                p1._lock._callmethod('release')
            except: pass
            try:
                p2._lock._callmethod('release')
            except: pass
            #print "core %d couldn't get lock for %16s" % (my_id,p1.name)
            time.sleep(1)
            continue
        elif not p2._lock._callmethod('acquire',(False,)):
            in_q.put((p1,p2))
            try:
                p1._lock._callmethod('release')
            except: pass
            try:
                p2._lock._callmethod('release')
            except: pass
            #print "core %d couldn't get lock for %16s" % (my_id,p2.name)
            time.sleep(1)
            continue
        print "core %d: running %16s vs %16s" % (my_id, p1.name, p2.name)
        res = 0
        now= time.time()
        for i in range(num_games):
            kill = time.time()
            r = playgame(p1,p2)
            sto = time.time()
            res += r
            if r:
                print "core %d: %16s beat %16s in %.2f secs" % (my_id, p1.name, p2.name,sto-kill)
            else:
                print "core %d: %16s beat %16s in %.2f secs" % (my_id, p2.name, p1.name,sto-kill)
        out_q.put((p1,p2,res,copy.deepcopy(p1.bot.my_stats),copy.deepcopy(p1.bot.opp_stats),copy.deepcopy(p1.bot.cory_stats),copy.deepcopy(p2.bot.my_stats),copy.deepcopy(p2.bot.opp_stats),copy.deepcopy(p2.bot.cory_stats)))
        p1._lock._callmethod('release')
        p2._lock._callmethod('release')
        print "core %d: ran %16s vs %16s and after %.2f secs, %s won %.2f of the time" % (my_id, p1.name, p2.name, time.time()-now, p1.name, res/float(num_games))

if __name__ == "__main__":
    m = 20 #number of games to run for
    
    num_cpus = cpu_count()
    match_queue = Queue()
    result_queue = Queue()

    bots = [Pokerbot(TheDerbs()),Pokerbot(ODoyleBot5()),Pokerbot(RockyBot3()),Pokerbot(LukeBotAgg3()),Pokerbot(MLKBot2Cool4U()),Pokerbot(MalcomXBot2()),Pokerbot(TheBostonDerby8())]
    test_bots = [Pokerbot(ManBearPigBot()),Pokerbot(ManBearPigBotNew())]
    n = len(bots)
    manager = Manager()
    run_bots = bots[:] + test_bots[:]
    for i,bot in enumerate(run_bots):
        bot._lock = manager.RLock()
        bot._index = i
    
    score = dict([(bot.name,dict([(x.name,[0,[],[],[]]) for x in run_bots])) for bot in run_bots])#,bot.bot.bot.eq_ranges]

    matchups = []
    for p1 in bots:
        for p2 in test_bots:
            if p2._index <= p1._index: continue
            matchups.append((p1,p2))

    random.shuffle(matchups)
    for match in matchups:
        match_queue.put(match)
    
    start = time.time()
    proc = []
    for l in range(num_cpus):
        p = Process(target=rungames, args=(l,m,match_queue,result_queue))
        proc.append(p)
        p.start()

    for i in range(len(matchups)):
        p1,p2,p1_wins,p1_my_stats,p1_opp_stats,p1_cory_stats,p2_my_stats,p2_opp_stats,p2_cory_stats = result_queue.get()
        score[p1.name][p2.name] = [p1_wins,p1_my_stats,p1_opp_stats,p1_cory_stats]
        score[p2.name][p1.name] = [m-p1_wins,p2_my_stats,p2_opp_stats,p2_cory_stats]
    
    for l in range(num_cpus):
        match_queue.put('STOP')

    print "finished in", time.time()-start
