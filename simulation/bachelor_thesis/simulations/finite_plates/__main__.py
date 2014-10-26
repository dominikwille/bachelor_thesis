#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from core.langevin_simulation import *
import csv


class FinitePlates(Langevin):
    # start position
    r = numpy.array([0.0, 0.0])
    # number of steps
    max_steps = 100000000
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

    max_c = 2000
    c_aa = [0] * max_c
    c_ab = [0] * max_c
    c_ad = [0] * max_c
    c_dd = [0] * max_c

    num_a = 0
    num_d = 0



    # Size of step  (variance ε)
    variance = 2 * d * D * step_size

    def boundary_condition(self, r_0, r_1):
        if abs(r_1[1]) > self.half_plate_distance and abs(r_1[0]) < self.l / 2:
            return True

        return False



    def boundary_position(self, r_0, r_1):
        if(r_1[1] > self.half_plate_distance):
            return numpy.array([r_1[0], self.half_plate_distance])
        else:
            return numpy.array([r_1[0], -self.half_plate_distance])

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
            # elif r_1[1] > self.half_plate_distance: # => from below
            #     y -= r_1[1] - self.half_plate_distance
            # elif r_1[1] < -self.half_plate_distance: # => from above
            #     y += -r_1[1] - self.half_plate_distance

        return numpy.array([x, y])

    def keep_absorbed(self):
        t = random.expovariate(1.0 / self.tao)
        return t

    def coordinate(self, r):
        if not self.absorbed:
            state = 0
        elif self.r[1] > 0:
            state = 1
        else:
            state = -1


        if self.step > self.max_c:
            if self.distances[0] == 1:
                self.num_a += 1
                i = 1
                while i <= self.max_c:
                    if (self.distances[i]) == (1):
                        self.c_aa[i - 1] += 1
                    elif (self.distances[i]) == (-1):
                        self.c_ab[i - 1] += 1
                    elif (self.distances[i]) == (0):
                        self.c_ad[i - 1] += 1
                    i += 1

            elif self.distances[0] == 0:
                self.num_d += 1
                i = 1
                while i <= self.max_c:
                    if (self.distances[i]) == 0:
                        self.c_dd[i - 1] += 1
                    i += 1
            self.distances.pop(0)
            self.steps.pop(0)


        return state


test = FinitePlates()
test.info_walk()
x = range(test.max_c)
y = test.c_aa

with open('test.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    data = [x, test.c_aa, test.c_ab, test.c_ad, test.c_dd]
    a.writerows(data)

test.c_aa = numpy.array(test.c_aa) / float(test.num_a)
test.c_ab = numpy.array(test.c_ab) / float(test.num_a)
test.c_ad = numpy.array(test.c_ad) / float(test.num_a)
test.c_dd = numpy.array(test.c_dd) / float(test.num_d)
# y = numpy.array(y) / float(num)

p0, = plt.plot(x, test.c_aa)
p1, = plt.plot(x, test.c_ab)
p2, = plt.plot(x, test.c_ad)
p3, = plt.plot(x, test.c_dd)
plt.legend([p0, p1, p2, p3], ['c_aa', 'c_ab', 'c_ad', 'c_dd'], loc=1)
plt.xlabel('Step')
plt.ylabel('Position')
# plt.ylim([-1.1, 1.1])
plt.show()