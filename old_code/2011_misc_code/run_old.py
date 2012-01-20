import os

if not os.path.exists(os.getcwd() + '/pokerbots/game'):
    os.mkdir(os.getcwd() + '/pokerbots/hh')
    os.mkdir(os.getcwd() + '/pokerbots/game')
    os.mkdir(os.getcwd() + '/pokerbots/util')
    os.mkdir(os.getcwd() + '/pokerbots/player')

from pokerbots.client.client import check_version, run

YOURBOT = 'flushbot'
OPPONENT = 'testbot'
print "playing ", YOURBOT, " vs ", OPPONENT
#check_version()
run(YOURBOT, OPPONENT)
