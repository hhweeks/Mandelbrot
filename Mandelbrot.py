import numpy as np
from PIL import Image, ImageDraw

"""
True/False convergence test
"""
def test_convergeance(c, maxiter):
    n = 0  # count iterations
    z = c

    while (abs(z) <= 2 and n < maxiter):
        z = z * z + c
        n += 1
    if (abs(z) > 2):  # catch diverging z on n=maxiter
        return False

    return True


"""
Num iterations convergeance function
"""
def iterations_to_convergeance(c, maxiter):
    n = 0
    z = c

    while (abs(z) <= 2 and n < maxiter):
        z = z * z + c
        n += 1

    return n


"""
loop over all complex vals given bounds
"""
def mset_from_bounds(maxiter, width, height, xstart, xend, ystart, yend, mystart, myheight):
    arr = np.empty((width, myheight), dtype=int)

    for i in range(0, width):
        for j in range(mystart, (mystart + myheight)):
            re = xstart + (i / width) * (xend - xstart)
            im = ystart + (j / height) * (yend - ystart)
            c = complex(re, im)

            color = iterations_to_convergeance(c, maxiter)

            col = j - mystart
            arr[i, col] = color

    return arr


"""
given an array of pixel val, draw image
ideas on how to map iterations to color via HSV from:
https://tech.io/playgrounds/2358/how-to-plot-the-mandelbrot-set/adding-some-colors
"""
def draw_array(arr, width, height, maxiter):
    image = Image.new('HSV', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    h = arr.shape[0]
    w = arr.shape[1]
    for i in range(w):
        for j in range(h):
            color = arr[i, j]
            hue = int(255 * color / maxiter)
            sat = 255
            value = 255 if color < maxiter else 0
            draw.point([i, j], (hue, sat, value))

    image.convert('RGB')
    image.show()


"""
original BW drawing of arr
"""
def draw_array_bw(arr, width, height, maxiter):
    image = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    h = arr.shape[0]
    w = arr.shape[1]
    for i in range(w):
        for j in range(h):
            color = arr[i, j]
            if color < maxiter:
                color = 255
            else:
                color = 0
            draw.point([i, j], (color, color, color))

    image.show()


"""
takes a list of tuples as args, (proc_num, resultsArr)
sorts on process number, concats arrays to draw
"""
def process_result_pairs(resultPairs, width, height, maxiter):
    resultPairs = sorted(resultPairs, key=lambda x: x[0])  # sort pairs by process number
    resultArrays = []
    for res in resultPairs:  # array of just result arrays
        resultArrays.append(res[1])

    resultsTuple = tuple(resultArrays)
    finalArray = np.concatenate((resultsTuple), axis=1)
    #draw_array_bw(finalArray, width, height, maxiter)
    draw_array(finalArray, width, height, maxiter)