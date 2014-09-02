from core.langevin_simulation import *
import matplotlib.pyplot as plt

def boundary(a, b):
    return False

def position(a, b):
    return False

def time():
    return False

def square(r):
    return r[0]**2

def step():
    return numpy.array([random.choice([1.0, -1.0])])

r_0 = numpy.array([0.0])
max_steps = 250
num = 1000

Y = numpy.array([0]*(max_steps + 1))
for i in range(num):
    x, y = info_walk(numpy.array([0.0]), max_steps, boundary, position, simple_step, time, square)
    Y = numpy.array(y) + Y


plt.plot(range(max_steps + 1), Y)
plt.xlabel('Step')
plt.ylabel('$\left<x^2 \\right>$')
plt.show()