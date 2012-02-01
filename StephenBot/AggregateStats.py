f = open("stats_normalized.txt", "r")
wf = open("aggregateStats_normalized.txt", "w")

stats = {}

l = f.readline()
while l:
    if l != "\n":
        line = l.split(" ")
        if line[0] not in stats.keys():
            stats[line[0]] = [[[],[],[]],
                              [[],[],[]],
                              [[],[],[]],
                              [[],[],[]]]
        stats[line[0]][int(line[2])][0] += [float(line[4])]
        stats[line[0]][int(line[2])][1] += [float(line[6])]
        stats[line[0]][int(line[2])][2] += [float(line[8])]
    l = f.readline()

for p in stats.keys():
    for s in [0,1,2,3]:
        wf.write(p+ " street: "+ str(s)+ " aggFreq: "+
                 str(sum(stats[p][s][0])/len(stats[p][s][0]))+ " avgChips "+
                 str(sum(stats[p][s][1])/len(stats[p][s][1]))+ " avgRaiseAmt: "+
                 str(sum(stats[p][s][2])/len(stats[p][s][2]))+ "\n")
    wf.write("\n")


for i in range(4):
    aggRank = []
    for p in stats.keys():
        aggRank += [(p, sum(stats[p][i][0])/len(stats[p][i][0]))] #aggFreq for player p

    sortedRanks = sorted(aggRank, key=lambda x: x[1])
    sortedRanks.reverse()
    wf.write("Sorted by aggFreq on street " + str(i) + "\n")
    for r in sortedRanks:
        wf.write(r[0] + " " + str(r[1]) + "\n")
    wf.write("\n")

