#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import numpy
import random


class Langevin(object):
    # This defines the dimension of the simulation
    d = 1
    # Size of on step (δt)
    dt = 1
    # start position
    r = [0]
    # number of steps
    max_steps = 100
    # list of performed steps
    steps = []
    # list of positions
    distances = []
    # Absorbed state
    absorbed = False
    # step
    step = 0
    # The probability that the particle absorbs if it fulfills the boundary condition
    p = 0.3
    # Diffusion constant
    D = 0.2


    def boundary_condition(self, r_0, r_1):
        raise NotImplementedError("Should have implemented this")

    def boundary_position(self, r_0, r_1):
        raise NotImplementedError("Should have implemented this")

    def next(self):
        raise NotImplementedError("Should have implemented this")

    def keep_absorbed(self):
        raise NotImplementedError("Should have implemented this")

    def coordinate(self, r):
        raise NotImplementedError("Should have implemented this")

    def add_step(self):
        self.steps.append(self.step)
        self.distances.append(self.coordinate(self.r))

    def info_walk(self):
        # Init steps and distances
        keep_absorbed = None
        self.steps = [self.step]
        self.distances = [self.coordinate(self.r)]
        # self.step += 1

        p = 0

        while self.step < self.max_steps:
            if p < self.step * 100 / self.max_steps:
                print p
                p += 1

            self.step += 1
            r_old = numpy.copy(self.r)
            if not self.absorbed:

                self.r += self.next()
                if self.boundary_condition(r_old, self.r):
                    if self.p > random.uniform(0.0, 1.0):
                        self.absorbed = True
                    else:
                        self.r = r_old
                        self.step -= 1
                        continue
                if not self.absorbed:
                    self.steps.append(self.step)
                    self.distances.append(self.coordinate(self.r))
            if self.absorbed:
                if keep_absorbed is None:
                    self.r = self.boundary_position(r_old, self.r)
                    keep_absorbed = int(self.keep_absorbed() / self.dt)
                elif(keep_absorbed > 0):
                    keep_absorbed -= 1
                else:
                    keep_absorbed = None
                    self.absorbed = False

                self.add_step()



        return self.steps, self.distances