from HandHistoryStatsCalculator import HandHistoryRePlayer
import multiprocessing as mp
import os,sys

def replayMatch(fname):
    if os.path.exists(fname):
        h = HandHistoryRePlayer(fname)
        return h.run()
    else:
        print >> sys.stderr, fname + " doesn't exist!"

if __name__ == "__main__":
    print sys.argv[1:]
    pool = mp.Pool()
    result = pool.map_async(replayMatch,sys.argv[1:])
    for r in result.get():
        print r
