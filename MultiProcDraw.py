import multiprocessing as mp
from Mandelbrot import mset_from_bounds, process_result_pairs
import timeit
from Bounds import WIDTH, HEIGHT, XSTART, XEND, YSTART, YEND, MAXITER, NUM_PROCS, P0HEIGHT, PNHEIGHT

"""
returns (process number, result array) via shared queue
"""
def parallel_draw(queue):
    rank = int(mp.current_process().name)
    myheight = P0HEIGHT if rank < NUM_PROCS - 1 else PNHEIGHT
    myhstart = rank * P0HEIGHT
    print("Process {} running with height {}".format(rank, myheight))
    arr = mset_from_bounds(MAXITER, WIDTH, HEIGHT, XSTART, XEND, YSTART, YEND, myhstart, myheight)

    tup = (rank, arr)
    queue.put(tup)


start_time = timeit.default_timer()
sharedQueue = mp.Queue()
processes = [mp.Process(target=parallel_draw, args=(sharedQueue,)) for x in range(NUM_PROCS)]

arrlist = []
i = 0
for p in processes:
    p.name = str(i)  # give process a rank so they know which piece of problem to work on
    p.start()
    i += 1

resultPairs = [sharedQueue.get() for p in processes]  # first=process number, second=array belonging to that process
process_result_pairs(resultPairs, WIDTH, HEIGHT, MAXITER)

elapsed_time = timeit.default_timer() - start_time
print("elapsed time {}".format(elapsed_time))
