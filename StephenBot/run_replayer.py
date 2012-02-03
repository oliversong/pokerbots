from HandHistoryRePlayer import HandHistoryRePlayer
import multiprocessing as mp
import os,sys

def replayMatch(fname):
    if os.path.exists(fname):
        h = HandHistoryRePlayer([fname])
        return h.run()
    else:
        print >> sys.stderr, fname + " doesn't exist!"

if __name__ == "__main__":
    print sys.argv[1:]
    for f in sys.argv[1:]:
        replayMatch(f)
    #pool = mp.Pool()
    #result = pool.map_async(replayMatch,sys.argv[1:])
    #f_out = open("stats_normalized.txt", 'a')
    #for r in result.get():
    #    f_out.write(r)
    #f_out.flush()
    #f_out.close()
