import multiprocessing as mp
from Mandelbrot import testConv
from PIL import Image, ImageDraw
import numpy as np

WIDTH=1000
HEIGHT=WIDTH
XSTART=-2
XEND=1
YSTART=-1.5
YEND=1.5
MAXITER=255#max int we can represent as a pixel value
NUM_PROCS=2
P0HEIGHT=HEIGHT//NUM_PROCS
PNHEIGHT=(HEIGHT//NUM_PROCS)+(HEIGHT%NUM_PROCS)#adjust for dimension not divis by NUM_PROCS

queue=mp.Queue()


def parallel_draw(q):
    num = int(mp.current_process().name)
    myheight = P0HEIGHT if num<NUM_PROCS-1 else PNHEIGHT
    myhstart = num*P0HEIGHT
    print("{} height {}".format(num,myheight))
    arr=np.empty((WIDTH,myheight),dtype=int)

    for i in range(0,WIDTH):
        for j in range(myhstart,(myhstart+myheight)):
            re = XSTART + (i/WIDTH) * (XEND - XSTART)
            im = YSTART + (j/HEIGHT) * (YEND - YSTART)
            c = complex(re,im)

            color=255
            if testConv(c, MAXITER):
                color=0
            col=j-myhstart
            arr[i,col]=color

    # q.put(num)
    q.put(arr)



image = Image.new('RGB', (WIDTH,HEIGHT),(0,0,0))
draw = ImageDraw.Draw(image)
processes = [mp.Process(target=parallel_draw, args=(queue,)) for x in range(NUM_PROCS)]

arrlist=[]
i=0
for p in processes:
    p.name=str(i)#give process a rank so they know which piece of problem to work on
    p.start()
    i+=1

for p in processes:
    pass
    #p.join()

results = [queue.get() for p in processes]
resultstup = tuple(results)
print("result shape {}".format(results[0].shape))
finalarr = np.concatenate((resultstup), axis=1)#TODO this doesn't put arrays back together in right order proc>2
print(finalarr.shape)

for i in range(WIDTH):
    for j in range(HEIGHT):
        color=finalarr[i,j]
        draw.point([i,j],(color,color,color))

image.show()

print(results)