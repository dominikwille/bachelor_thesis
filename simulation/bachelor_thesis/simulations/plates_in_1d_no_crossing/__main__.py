import matplotlib.pyplot as plt
import numpy
import random
from core.langevin_simulation import *

def P():
    tao = 0.03
    t = random.expovariate(tao)
    return t

def plate_position(r_0, r_1):
    plate_0 = 5.0
    plate_1 = -5.0
    if (r_1 >= plate_0):
        plate = plate_0
    elif (r_1 <= plate_1):
        plate = plate_1
    else:
        plate = 0
    return numpy.array([plate])

def plate_boundary(r_0, r_1):
    return numpy.linalg.norm(r_1) >= 5

def first_component(r):
    return r[0]

def square(r):
    return r[0]**2

r_0 = numpy.array([5.0])
max_steps = 10000

x, y = info_walk(r_0, max_steps, plate_boundary, plate_position, simple_step, P, first_component)

Y = []
last_item = 0
step = 0
for i in y:
    step += 1
    last_item = i**2 + last_item
    Y.append(last_item / step)

plt.plot(x, Y)
plt.plot(x, y)
plt.xlabel('Step')
plt.ylabel('Position')
plt.ylim([-6, 36])
plt.show()