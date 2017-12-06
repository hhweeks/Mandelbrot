import multiprocessing as mp
from Mandelbrot import testConv
from PIL import Image, ImageDraw
import numpy as np
import timeit

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

sharedQueue=mp.Queue()


def parallel_draw(queue):
    num = int(mp.current_process().name)
    myheight = P0HEIGHT if num<NUM_PROCS-1 else PNHEIGHT
    myhstart = num*P0HEIGHT
    print("{} height {}".format(num,myheight))
    # arr=np.empty((WIDTH,myheight),dtype=int)
    arr=calcConvergeance(MAXITER,WIDTH,HEIGHT,XSTART,XEND,YSTART,YEND,myhstart,myheight)

    #put this draw loop in its own function where it can be called by serial or parallel
    # for i in range(0,WIDTH):
    #     for j in range(myhstart,(myhstart+myheight)):
    #         re = XSTART + (i/WIDTH) * (XEND - XSTART)
    #         im = YSTART + (j/HEIGHT) * (YEND - YSTART)
    #         c = complex(re,im)
    #
    #         color=255
    #         if testConv(c, MAXITER):
    #             color=0
    #         col=j-myhstart
    #         arr[i,col]=color

    # q.put(num)
    tup=(num,arr)
    queue.put(tup)

def calcConvergeance(maxiter, width, height, xstart, xend, ystart, yend, mystart, myheight):

    arr=np.empty((WIDTH,myheight),dtype=int)

    for i in range(0,width):
        for j in range(mystart,(mystart+myheight)):
            re = xstart + (i/width) * (xend - xstart)
            im = ystart + (j/height) * (yend - ystart)
            c = complex(re,im)
            color=255
            if testConv(c, maxiter):
                color=0
            col=j-mystart
            arr[i,col]=color

    return arr

#given an array of pixel val, draw image
def drawArr(arr):
    h=arr.shape[0]
    w=arr.shape[1]
    for i in range(w):
        for j in range(h):
            color=arr[i, j]
            draw.point([i,j],(color,color,color))


start_time= timeit.default_timer()

image = Image.new('RGB', (WIDTH,HEIGHT),(0,0,0))
draw = ImageDraw.Draw(image)
processes = [mp.Process(target=parallel_draw, args=(sharedQueue,)) for x in range(NUM_PROCS)]

arrlist=[]
i=0
for p in processes:
    p.name=str(i)#give process a rank so they know which piece of problem to work on
    p.start()
    i+=1

for p in processes:
    pass
    # p.join()

resultPairs = [sharedQueue.get() for p in processes]#first=process number, second=array belonging to that process
resultPairs = sorted(resultPairs, key=lambda x: x[0])#sort pairs by process number
resultArrays = []
for res in resultPairs:
    resultArrays.append(res[1])


resultstup = tuple(resultArrays)

finalArray = np.concatenate((resultstup), axis=1)
print(finalArray.shape)

drawArr(finalArray)

elapsed_time = timeit.default_timer() - start_time
print("elapsed time {}".format(elapsed_time))

image.show()
