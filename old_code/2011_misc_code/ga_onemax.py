#    This file is part of EAP.
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.

import random,time
from multiprocessing import Process, Queue, cpu_count, Value
#from pokerbots.engine.game import Card, Board, Check
from pokerbots.engine.game import Table
from pokerbots.player.pokerbot import Pokerbot
from pokerbots.player.BostonDerby_old import TheBostonDerby8
from pokerbots.player.LukeBotAgg import LukeBotAgg
from eap import base
from eap import creator
from eap import toolbox
from eap import algorithms

bot = Pokerbot(LukeBotAgg())
test_bots = [Pokerbot(TheBostonDerby8())]
num_cpus = cpu_count()

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
creator.create("Population", list)
def gen():
    return sorted([random.randint(1,20)*5 for y in range(4)])
    #return random.randint(1,20)*5
tools = toolbox.Toolbox()
# Attribute generator
tools.register("attr_bool", gen)
# Structure initializers
tools.register("individual", creator.Individual,
    content_init=tools.attr_bool, size_init=4)
tools.register("population", creator.Population,
    content_init=tools.individual, size_init=50)

def playgame(p1, p2):
    t = Table(p1, p2, False)
    t.play_match()
    return t.p2.stack == 0 #return 1 if p1 won, 0 if p2 won

def rungames(p1,p2,num_games,output):
    res = 0
    for i in range(num_games):
        res += playgame(p1,p2)
    while not output.acquire(): continue
    output.value += res
    output.release()

def evalOneMax(individual):
    bot.bot.bot.eq_ranges=individual
    p1_wins = Value('i',0)#[resultsaccum() for i in range(num_cpus)]
    res = 0
    m = 10
    for p2 in test_bots:
        now= time.time()
        games_to_run = m
        proc = []
        p1_wins = Value('i',0)#[resultsaccum() for i in range(num_cpus)]

        for l in range(num_cpus-1):
            p = Process(target=rungames, args=(bot,p2,m/num_cpus,p1_wins))
            proc.append(p)
            p.start()
            games_to_run = games_to_run - m/num_cpus
        
        #print games_to_run
        rungames(bot,p2,m/num_cpus,p1_wins)

        for p in proc:
            p.join()
        res += p1_wins.value
    return res,
        

# Operator registering
tools.register("evaluate", evalOneMax)
tools.register("mate", toolbox.cxTwoPoints)
tools.register("mutate", toolbox.mutShuffleIndexes, indpb=0.05)
tools.register("select", toolbox.selTournament, tournsize=3)


if __name__ == "__main__":
    random.seed(64)
    
    pop = tools.population()
    CXPB, MUTPB, NGEN = 0.5, 0.2, 10
    
    print "Start of evolution"
    begin = time.time()
    #algorithms.eaSimple(tools, pop, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN)
    
    if 1:
        # Evaluate the entire population
        fitnesses = tools.map(tools.evaluate, pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        
        print "  Evaluated %i individuals in %.2f secs" % (len(pop), time.time()-begin)
        
        # Begin the evolution
        for g in range(NGEN):
            print "-- Generation %i --" % g
            
            start = time.time()
            # Select the next generation individuals
            offsprings = tools.select(pop, n=len(pop))
            # Clone the selected individuals
            offsprings = map(tools.clone, offsprings)
        
            # Apply crossover and mutation on the offsprings
            for child1, child2 in zip(offsprings[::2], offsprings[1::2]):
                if random.random() < CXPB:
                    tools.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offsprings:
                if random.random() < MUTPB:
                    tools.mutate(mutant)
                    del mutant.fitness.values
        
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offsprings if not ind.fitness.valid]
            fitnesses = map(tools.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            print "  Evaluated %i individuals in %.2f secs" % (len(invalid_ind),time.time()-start)
            
            # The population is entirely replaced by the offsprings
            pop[:] = offsprings
            
            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.values[0] for ind in pop]
            
            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std_dev = abs(sum2 / length - mean**2)**0.5
            
            print "  Min %s" % min(fits)
            print "  Max %s" % max(fits)
            print "  Avg %s" % mean
            print "  Std %s" % std_dev
        
    print "-- End of (successful) evolution -- (%.2f)" % time.time()-begin
        
    best_ind = toolbox.selBest(pop, 1)[0]
    print "Best individual is %s, %s" % (best_ind, best_ind.fitness.values)

