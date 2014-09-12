#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from core.langevin_simulation import *
import matplotlib.pyplot as plt


class MeanSquare(Langevin):
    # start position
    r = numpy.array([-1.0])
    # number of steps
    max_steps = 400
    # list of performed steps
    steps = []
    # list of positions
    distances = []
    # Absorbed state
    absorbed = False
    # This defines the dimension of the simulation
    d = 3

    # Diffusion constant
    D = 0.1
    # Size of on step - 1/resolution (δt)
    dt = 20.0

    # Size of step  (variance ε)
    e = (2 * d * D * dt)**0.5

    def boundary_condition(self, r_0, r_1):
        return False

    def next(self):
        mean = 0
        r = [0] * self.d
        component = random.choice(range(self.d))
        r[component] = random.gauss(mean, self.e)
        return numpy.array(r)

    def coordinate(self, r):
        return numpy.linalg.norm(r)**2

test = MeanSquare()
test.max_steps = 1000
num = 5001
nums = [50, 500, 5000]
Y_e = []
Y = numpy.array([0]*(test.max_steps + 1))
for i in range(num):
    print i
    test.step = 0
    test.r = numpy.array([0.0]*test.d)
    x, y = test.info_walk()
    Y = numpy.array(y) + Y
    if i in nums:
        Y_e.append(Y / i)


Y /= num

y_a = numpy.array(x) * 2 * test.D * test.d * test.dt

p0, = plt.plot(range(test.max_steps + 1), Y_e[0])
p1, = plt.plot(range(test.max_steps + 1), Y_e[1])
p2, = plt.plot(range(test.max_steps + 1), Y_e[2])
pa, = plt.plot(x, y_a)
plt.legend([p0, p1, p2, pa], [str(nums[0]) + ' runs', str(nums[1]) + ' runs', str(nums[2]) + ' runs', 'analytic'], loc=2)
plt.xlabel('Step')
plt.ylabel('$\left<x^2 \\right>$')
plt.show()