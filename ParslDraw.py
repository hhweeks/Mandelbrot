from parsl import *
import timeit
from Mandelbrot import mset_from_bounds, process_result_pairs
from Bounds import WIDTH, HEIGHT, XSTART, XEND, YSTART, YEND, MAXITER, NUM_PROCS, P0HEIGHT, PNHEIGHT

workers = ThreadPoolExecutor(max_workers=NUM_PROCS)
dfk = DataFlowKernel(executors=[workers])

"""
returns (process number, result array)
"""
@App('python', dfk)
def parallel_draw(rank):
    myheight = P0HEIGHT if rank < NUM_PROCS - 1 else PNHEIGHT
    myhstart = rank * P0HEIGHT
    print("Process {} running with height {}".format(rank, myheight))
    arr = mset_from_bounds(MAXITER, WIDTH, HEIGHT, XSTART, XEND, YSTART, YEND, myhstart, myheight)
    tup = (rank, arr)
    return tup


start_time = timeit.default_timer()

resultPairs = []
app_futures = []

for i in range(0, NUM_PROCS):
    app_futures.append(parallel_draw(i))

for i in range(NUM_PROCS):
    resultPairs.append(app_futures[i].result())

process_result_pairs(resultPairs, WIDTH, HEIGHT, MAXITER)

elapsed_time = timeit.default_timer() - start_time
print("elapsed time {}".format(elapsed_time))
