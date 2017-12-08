from Mandelbrot import mset_from_bounds, process_result_pairs
import timeit
from Bounds import WIDTH, HEIGHT, XSTART, XEND, YSTART, YEND, MAXITER, NUM_PROCS, P0HEIGHT, PNHEIGHT


def serial_draw():
    pass
    arr = mset_from_bounds(MAXITER, WIDTH, HEIGHT, XSTART, XEND, YSTART, YEND, 0, HEIGHT)
    tup = (0, arr)
    return tup


start_time = timeit.default_timer()

resultPair = []
resultPair.append(serial_draw())
process_result_pairs(resultPair, WIDTH, HEIGHT, MAXITER)

elapsed_time = timeit.default_timer() - start_time
print("elapsed time {}".format(elapsed_time))
