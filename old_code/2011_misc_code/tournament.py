"""

tournament.py
Script to run a tournament and measure a number of variables

"""

from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
from size import asizeof
import time
import csv
import sys
    
from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
from random import randint
import time
from multiprocessing.sharedctypes import synchronized
from Queue import Empty
from multiprocessing import Process, Queue, cpu_count, Value, Manager
import os, copy,random
for bot in os.listdir('./pokerbots/player/'):
    f = bot.split(".")
    if len(f) == 2 and f[1] == "py" and f[0]:
        exec("from pokerbots.player."+f[0]+" import *")

def run_tournament(s1, s2):
    f1 = open('scrim_' + str(s1) + '_' + str(s2) + '.csv', 'wb')
    f2 = open('log_' + str(s1) + '_' + str(s2) + '.csv', 'wb')
    data = csv.writer(f1, delimiter=',')
    data.writerow(['Seat 1', 'Seat 2', 'Match', 'Duration', 'Hands', 
                   'Seat 1 Response', 'Seat 2 Response', 'Seat 1 Actions',
                   'Seat 2 Actions', 'Seat 1 Memory', 'Seat 2 Memory', 
                   'Winner', 'Loser'])
    out = csv.writer(f2, delimiter=',')
    out.writerow(['Seat 1', 'Seat 2', 'Success'])

    MATCHES = 2

    submissions = [TheDerbs(),ODoyleBot3(),ODoyleBot2(),ODoyleBot1(),ODoyleBot4(),ODoyleBot5(),RockyBot2(),RockyBot4(),RockyBot3(),ManBearPigBot(),ManBearPigBot1(),ManBearPigBot2(),LukeBotAgg(),LukeBotAgg1(),LukeBotAgg2(),LukeBotAgg3(),MLKBot2(),MLKBot2Cool4U(),MalcomXBot(),MalcomXBot1(),MalcomXBot2(),TheBostonDerbyA(),TheBostonDerbyB(),TheBostonDerbyC(),LukesDerby(),LukesDerby1(),LukesDerby2(),LukesDerby3(),LukesDerby4(),LukesDerby5(),LukesDerby6(),LukesDerby7(),LukesDerby8(),TheBostonDerby0(),TheBostonDerby1(),TheBostonDerby2(),TheBostonDerby3(),TheBostonDerby4(),TheBostonDerby5(),TheBostonDerby6(),TheBostonDerby7(),TheBostonDerby8()]
    print len(submissions)
    num_cpus = cpu_count()
    match_queue = Queue()
    result_queue = Queue()
    manager = Manager()

    bots = []
                  

    # instantiate all bots
    for i,team in enumerate(submissions):
        bot = Pokerbot(team)
        bot._lock = manager.RLock()
        bot._index = i
        bots.append(bot)

    print "finished instantiating bots"

    matchups = []
    for p1 in bots[:-1]:
        for p2 in bots:
            if p2._index <= p1._index: continue
            matchups.append((p1,p2))

    random.shuffle(matchups)
    for match in matchups:
        match_queue.put(match)
    
    proc = []
    for l in range(num_cpus):
        p = Process(target=rungames, args=(l,MATCHES,match_queue,result_queue))
        proc.append(p)
        p.start()

    for i in range(len(matchups)):
        while True:
            try:
                metrics,logs = result_queue.get(False,.2)
                break
            except Empty:
                time.sleep(.1)
        for stat in metrics:
            data.writerow(stat)
        for output in logs:
            out.writerow(output)
    
    for l in range(num_cpus):
        match_queue.put('STOP')
    
    for p in proc:
        p.join()
    
    f1.close()
    f2.close()



def rungames(my_id,MATCHES,in_q,out_q):
    match_count = 1
    for p1,p2 in iter(in_q.get, 'STOP'):
        if p1 == p2: continue
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
        print "core %d running %16s vs %16s" % (my_id, p1.name, p2.name)
        metrics = []
        log = []
        for i in range(1, MATCHES+1):
            start_time = time.time()
            t = Table(p1, p2, False)
            while t.p1.stack > 0 and t.p2.stack > 0:
                t.play()
            end_time = time.time()
            if t.p1.stack == 0:
                winner = t.p2.name
                loser = t.p1.name
            else:
                winner = t.p1.name
                loser = t.p2.name
            stats = [t.p1.name, t.p2.name, str(i),
                     str(end_time-start_time), str(t.hands_played),
                     #str(float(t.p1.time)/t.p1.num_actions),
                     #str(float(t.p2.time)/t.p2.num_actions),
                     str(t.p1.num_actions),
                     str(t.p2.num_actions),
                     str(asizeof(t.p1.bot)),
                     str(asizeof(t.p2.bot)), winner, loser]
            metrics.append(stats)
            #data.writerow(stats)
            print 'Match #' + str(match_count) + ' complete, ' + winner + ' beats ' + loser
            output = [t.p1.name, t.p2.name, 'True']
            #out.writerow(output)
            match_count += 1
            try:
                match_count = match_count
            except:
                t.p1.stack = 0
                t.p2.stack = 0
                print 'Match #' + str(match_count) + ' failed'
                print 'Offenders were ' + t.p1.name + ' & ' + t.p2.name
                output = [t.p1.name, t.p2.name, 'False']
                stats = []
                #out.writerow(output)
                match_count += 1
            log.append(output)
        out_q.put((metrics,log))
        p1._lock._callmethod('release')
        p2._lock._callmethod('release')
