from PIL import Image, ImageDraw
from Mandelbrot import testConv
width=1000
height=1000
xstart=-2
xend=1
ystart=-1.5
yend=1.5
maxiter=255#max int we can represent as a pixel value

image = Image.new('RGB', (width,height),(0,0,0))
draw = ImageDraw.Draw(image)

for i in range(0,width):
    for j in range(0,height):
        re = xstart + (i/width) * (xend - xstart)
        im = ystart + (j/height) * (yend - ystart)
        c = complex(re,im)

        color=255
        if testConv(c, maxiter):
            color=0
        draw.point([i,j],(color,color,color))

image.show()
#image.save('output.png','PNG')