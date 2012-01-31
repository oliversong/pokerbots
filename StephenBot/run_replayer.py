from HandHistoryRePlayer import HandHistoryRePlayer
import multiprocessing as mp
import os,sys

def replayMatch(fname):
    if os.path.exists(fname):
        h = HandHistoryRePlayer(fname)
        h.run()

if __name__ == "__main__":
    print sys.argv[1:]
    pool = mp.Pool()
    pool.map(replayMatch,sys.argv[1:])
