import parsl
from parsl import *
from MultiProcDraw import calcConvergeance, drawArr
import numpy as np

workers= ThreadPoolExecutor(max_workers=4)
dfk= DataFlowKernel(executors=[workers])

WIDTH=1400
HEIGHT=WIDTH
XSTART=-2
XEND=1
YSTART=-1.5
YEND=1.5
MAXITER=255#max int we can represent as a pixel value
NUM_PROCS=4
P0HEIGHT=HEIGHT//NUM_PROCS
PNHEIGHT=(HEIGHT//NUM_PROCS)+(HEIGHT%NUM_PROCS)#adjust for dimension not divis by NUM_PROCS

@App('python', dfk)
def parallel_draw(rank):
    myheight = P0HEIGHT if rank<NUM_PROCS-1 else PNHEIGHT
    myhstart = rank*P0HEIGHT
    print("{} height {}".format(rank,myheight))
    arr=calcConvergeance(MAXITER,WIDTH,HEIGHT,XSTART,XEND,YSTART,YEND,myhstart,myheight)
    return arr

#app_future = parallel_draw(0)
resultPairs=[]
for i in range(NUM_PROCS):
    resultPairs.append(parallel_draw(i))

resultPairs = sorted(resultPairs, key=lambda x: x[0])#sort pairs by process number
resultArrays = []
for res in resultPairs:
    resultArrays.append(res[1])


resultstup = tuple(resultArrays)

finalArray = np.concatenate((resultstup), axis=1)
print(finalArray.shape)

drawArr(finalArray)

# Check status
#print("Status: ", app_future.done())

# Get result
#print("Result: ", app_future.result())