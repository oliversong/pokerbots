from pokerbots.engine.game import Raise, Check, Call, Bet, Fold, Deal, Show, Won, Post
from pokerbots.player.ourbot import TheBostonDerby
import os,csv

US = 'TheBostonDerby1'

def evaluate(gm,us,opp):
    in_file = open(gm,"r")
    lines = in_file.readlines()

    hand = []
    game = []

    for i in range(3,len(lines)-1):
        if not lines[i].strip():
            game.append(hand)
            hand = []
        else:
            text = lines[i]
            hand.append(text)

    match = []
    for i in range(0,len(game)):
        actions = []
        for j in range(0,len(game[i])):
            descrip = game[i][j].split()
            #print descrip
            #raw_input()
            if descrip[0] == '***':
                actions.append(["Dealer", "blah"])
            elif descrip[0] in [us,opp]:
                if descrip[1] == "folds" or descrip[1] == "checks":
                    actions.append([descrip[0], descrip[1]])
                elif descrip[1] == "posts":
                    actions.append([descrip[0],descrip[1]+" "+descrip[6].replace(",","")])
                elif descrip[1] == "bets" or descrip[1] == "calls":
                    if descrip[2][-1] == ',':
                        actions.append([descrip[0], descrip[1]+" "+descrip[2].replace(",","")])
                    else:
                        actions.append([descrip[0], descrip[1]+" "+descrip[2]])
                elif descrip[1] == "raises":
                    actions.append([descrip[0], descrip[1]+" "+descrip[3].replace(",","")])
                elif descrip[1] == "wins":
                    actions.append([descrip[0], descrip[1]+" "+descrip[4].replace("(","").replace(")","")])
                elif descrip[1] == "ties":
                    actions.append([descrip[0], 'wins'+" "+descrip[5].replace("(","").replace(")","")])
            #print actions
        match.append(actions)
        
    new_actions = match[:]
    actions = match[:]
    for i in range(0,len(match)):
        for j in range(0,len(match[i])):
            if new_actions[i][j][0] == "Dealer":
                actions[i][j][1] = Deal([])
            elif new_actions[i][j][1] == "folds":
                actions[i][j][1] = Fold()
            elif new_actions[i][j][1] == "checks":
                actions[i][j][1] = Check()
            elif new_actions[i][j][1].split()[0] == "posts":
                actions[i][j][1] = Post(int(actions[i][j][1].split()[1]))
            elif new_actions[i][j][1].split()[0] == "bets":
                actions[i][j][1] = Bet(int(actions[i][j][1].split()[1]))
            elif new_actions[i][j][1].split()[0] == "calls":
                actions[i][j][1] = Call()
            elif new_actions[i][j][1].split()[0] == "raises":
                actions[i][j][1] = Raise(int(actions[i][j][1].split()[1]))
            elif new_actions[i][j][1].split()[0] == "wins":
                actions[i][j][1] = Won(int(actions[i][j][1].split()[1]))

    return actions

if __name__ == "__main__":
    pre = './pokerbots/hh/'
    matches = sorted([m for m in os.listdir(pre+US) if len(m.split('.'))>2],key=lambda x:x.split(".")[-2])
    stats= {}
    for i in range(len(matches)):
        opp = matches[i].split(".")[0]
        hands = evaluate(pre+US+"/"+matches[i],US,opp)
        bot = TheBostonDerby()
        bot.opponent = {'name':opp}
        bot.name = US
        for j in range(len(hands)):
            if len(hands[j]) < 4:
                print hands[j]
                raw_input()
            bot.calculate_stats(hands[j])
        if not stats.has_key(opp):
            stats[opp] = []
        stats[opp].append((bot.my_stats,bot.opp_stats,bot.cory_stats))
    f = open('test.csv','w')
    g = open('us.csv','w')
    f.write(reduce(lambda x, y: x+","+y,['opp']+[m for m in bot.my_stats.keys()+bot.cory_stats.keys() if m[0] not in ['^','_']])+"\n")
    g.write(reduce(lambda x, y: x+","+y,['opp']+[m for m in bot.my_stats.keys() if m[0] not in ['^','_']])+"\n")
    c = csv.DictWriter(f,['opp']+[m for m in bot.my_stats.keys()+bot.cory_stats.keys() if m[0] not in ['^','_']],extrasaction='ignore')
    k = csv.DictWriter(g,['opp']+[m for m in bot.my_stats.keys() if m[0] not in ['^','_']],extrasaction='ignore')
    for opp in stats.keys():
        for d in stats[opp]:
            e = d[1]
            e.update(d[2])
            e['opp'] = opp
            c.writerow(e)
    for opp in stats.keys():
        for d in stats[opp]:
            e = d[0]
            e['opp'] = opp
            k.writerow(e)
    f.close()
    g.close()
