#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from core.langevin_simulation import *


class Plates1dNoCrossing(Langevin):
    # start position
    r = numpy.array([-1.0])
    # number of steps
    max_steps = 400
    # list of performed steps
    steps = []
    # list of positions
    distances = []
    # Absorbed state
    absorbed = True
    # This defines the dimension of the simulation
    d = 1

    # Plate distance
    half_plate_distance = 1.0
    # Diffusion constant
    D = 1.0
    # Size of on step - 1/resolution (δt)
    step_size = 0.1
    # Parameter of the exponential decaying desorbtion probability
    tao = 30
    # The probability that the particle absorbs if it fulfills the boundary condition
    p = 0.3

    # Size of step  (variance ε)
    variance = 2 * d * D * step_size

    def boundary_condition(self, r_0, r_1):
        return abs(r_1[0]) >= self.half_plate_distance

    def boundary_position(self, r_0, r_1):
        plate_0 = self.half_plate_distance
        plate_1 = -self.half_plate_distance
        if (r_1 >= plate_0):
            plate = plate_0
        elif (r_1 <= plate_1):
            plate = plate_1
        else:
            plate = 0
        return numpy.array([plate])

    def next(self):
        #return numpy.array([random.choice([-self.variance, self.variance])])
        mean = 0

        r = []
        i = 0
        while i < self.d:
            i += 1
            r.append(random.gauss(mean, self.variance))

        return numpy.array(r)

    def keep_absorbed(self):
        t = random.expovariate(1.0 / self.tao)
        return t

    def coordinate(self, r):
        return r[0]


test = Plates1dNoCrossing()
x, y = test.info_walk()

plt.plot(x, y)
plt.xlabel('Step')
plt.ylabel('Position')
plt.ylim([-1.1, 1.1])
plt.show()