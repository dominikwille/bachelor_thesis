#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from core.langevin_simulation import *


class FinitePlates(Langevin):
    # start position
    r = numpy.array([0.0, 0.0])
    # number of steps
    max_steps = 4000
    # list of performed steps
    steps = []
    # list of positions
    distances = []
    # Absorbed state
    absorbed = False
    # This defines the dimension of the simulation
    d = 2

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

    l = 10.0

    L = 15.0

    # Size of step  (variance ε)
    variance = 2 * d * D * step_size

    def boundary_condition(self, r_0, r_1):
        # if abs(r_1[1]) > self.half_plate_distance and abs(r_1[0]) < self.l / 2:
        #     return True

        return False



    def boundary_position(self, r_0, r_1):
        return numpy.array([0, 0])

    def next(self):
        mean = 0
        l = random.gauss(mean, self.variance)
        phi = random.random() * numpy.pi
        x = numpy.cos(phi) * l
        y = numpy.sin(phi) * l

        r_1 = [x + self.r[0], y + self.r[1]]

        # Right - Left
        if r_1[0] >= self.L/2:
            x -= r_1[0] - self.L/2
        if r_1[0] <= -self.L/2:
            x += -r_1[0] - self.L/2

        # Top - Bottom
        if r_1[1] >= self.L/2:
            y -= r_1[1] - self.L/2
        if r_1[1] <= -self.L/2:
            y += - r_1[1] - self.L/2

        # Rods
        if abs(r_1[1]) > self.half_plate_distance and abs(r_1[0]) < self.l / 2:
            if self.r[0] >= self.l / 2: # => from the right
                x += self.l / 2 - r_1[0]
            elif self.r[0] <= -self.l / 2: # => from the left
                x -= r_1[0] + self.l / 2
            elif r_1[1] > self.half_plate_distance: # => from below
                y -= r_1[1] - self.half_plate_distance
            elif r_1[1] < -self.half_plate_distance:
                y += -r_1[1] - self.half_plate_distance

        return numpy.array([x, y])

    def keep_absorbed(self):
        t = random.expovariate(1.0 / self.tao)
        return t

    def coordinate(self, r):
        return numpy.copy(r)


test = FinitePlates()
n, data = test.info_walk()
data = numpy.matrix(data)
x = data[:, 0]
y = data[:, 1]

plt.plot(x, y)
plt.xlabel('Step')
plt.ylabel('Position')
# plt.ylim([-1.1, 1.1])
plt.show()