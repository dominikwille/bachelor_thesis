#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from core.langevin_simulation import *
import matplotlib.pyplot as plt


class MeanSquare(Langevin):
    def boundary_condition(self, r_0, r_1):
        return False

    def step(self):
        mean = 0
        variance = 2

        r = []
        i = 0
        while i < self.D:
            i += 1
            r.append(random.gauss(mean, variance))

        return numpy.array(r)
        # return numpy.array([random.choice([1.0, -1.0])])

    def coordinate(self, r):
        return r[0]**2

test = MeanSquare()
test.step_size = 1
test.max_steps = 1000
num = 1000

Y = numpy.array([0]*(test.max_steps + 1))
for i in range(num):
    test.r = numpy.array([0.0])
    x, y = test.info_walk()
    Y = numpy.array(y) + Y

Y /= num

x_a = numpy.arange(0, test.max_steps, 1)
y_a = x_a * 4

plt.plot(range(test.max_steps + 1), Y)
plt.plot(x_a, y_a)
plt.xlabel('Step')
plt.ylabel('$\left<x^2 \\right>$')
plt.show()