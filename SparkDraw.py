from Mandelbrot import mset_from_bounds, process_result_pairs
from pyspark.sql import SparkSession
from pyspark import SparkContext
from Bounds import WIDTH, HEIGHT, XSTART, XEND, YSTART, YEND, MAXITER, NUM_PROCS, P0HEIGHT, PNHEIGHT

def map_draw(rank):
    myheight = P0HEIGHT if rank < NUM_PROCS - 1 else PNHEIGHT
    myhstart = rank * P0HEIGHT
    print("{} height {}".format(rank, myheight))
    arr = mset_from_bounds(MAXITER, WIDTH, HEIGHT, XSTART, XEND, YSTART, YEND, myhstart, myheight)
    tup = (rank, arr)
    return tup

#spark = SparkSession.builder.appName("SparkDraw").getOrCreate()
sc = SparkContext("local", "SparkDraw")
resultArr =[]
resultArr.append(sc.parallelize(range(0,NUM_PROCS)).map(map_draw(0)).collect())#TODO input range val into map
"""
incomplete solution, collection on this RDD is causing serialization issues?
"""
print("result {}".format(resultArr))
process_result_pairs(resultArr, WIDTH, HEIGHT, MAXITER)

sc.stop()

