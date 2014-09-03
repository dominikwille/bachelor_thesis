#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from core.langevin_simulation import *


class Plates1dNoCrossing(Langevin):
    # start position
    r = numpy.array([5])
    # number of steps
    max_steps = 100000
    # list of performed steps
    steps = []
    # list of positions
    distances = []

    # This defines the dimension of the simulation
    d = 1
    # Plate distance
    plate_distance = 1.0
    # Diffusion constant
    D = 1.0

    # Size of on step / resolution (δt)
    step_size = 1

    # Size of step  (variance ε)
    variance = (2 * d * D * step_size)**0.5

    def boundary_condition(self, r_0, r_1):
        return numpy.linalg.norm(r_1) >= 5

    def boundary_position(self, r_0, r_1):
        plate_0 = 5.0
        plate_1 = -5.0
        if (r_1 >= plate_0):
            plate = plate_0
        elif (r_1 <= plate_1):
            plate = plate_1
        else:
            plate = 0
        return numpy.array([plate])

    def step(self):
        mean = 0

        r = []
        i = 0
        while i < self.d:
            i += 1
            r.append(random.gauss(mean, self.variance))

        return numpy.array(r)
        # return numpy.array([random.choice([1.0, -1.0])])

    def keep_absorbed(self):
        tao = 0.03
        t = random.expovariate(tao)
        return t

    def coordinate(self, r):
        return r[0]


test = Plates1dNoCrossing()

x, y = test.info_walk()

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