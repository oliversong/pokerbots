import matplotlib.pylab as plt
import sys

round1 = sys.argv[1]
round2 = None
round3 = None

p1 = ""
p2 = ""
p3 = ""

banks = {}

plt.figure(None, (23,12))


if len(sys.argv)==4:
    round2 = sys.argv[2]
    round3 = sys.argv[3]
    plt.subplot(311)

def readHandHistory(r):
    global p1
    global p2
    global p3
    f = open(r, 'r')
    line = f.readline()
    while line:
        line = line.split(" ")
        if line[0] == "6.S912":
            p1 = line[4]
            p2 = line[6]
            p3 = line[8][:-1] #get rid of new line char
            banks[p1] = [banks[p1][0]] if p1 in banks.keys() else ['r--']
            banks[p2] = [banks[p2][0]] if p2 in banks.keys() else ['bs']
            banks[p3] = [banks[p3][0]] if p3 in banks.keys() else ['g^']
        if line[0]=="Seat":
            banks[line[3][:-4]] += [line[-1]]
    

        line = f.readline()
    t = [i for i in range(len(banks[p1])-1)]
    plt.plot(t, banks[p1][1:], banks[p1][0], t, banks[p2][1:], banks[p2][0], t, banks[p3][1:], banks[p3][0])
    plt.legend((p1, p2, p3), loc='upper left')


readHandHistory(round1)

if round2 and round3:
    plt.subplot(312)
    readHandHistory(round2)
    plt.subplot(313)
    readHandHistory(round3)

if p2 and p3:
    plt.savefig(p1+" vs. "+p2+" vs. "+p3+".png")
else:
    plt.savefig(p1+".png")


