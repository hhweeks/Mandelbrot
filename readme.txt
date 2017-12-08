Computation of the Mandelbrot set using:
Serial execution
Python multiprocessic
Parsl

The scripts SerialDraw, MultiProcDraw, and ParslDraw each calculate the Mandelbrot set using the approach their name indicates. Shared functions for calculating the set are in Mandelbrot.py. Written and tested with Python 3.6.1. Parameters can be changed in the Bounds.py file.

1400x1400 canvas, with 4 processes and a max iteration of 100:
Serial 20.7s
MultiProcessing 13.7s
Parsl 20.4s
