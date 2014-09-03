#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import numpy
import random


class Langevin(object):
    # This defines the dimension of the simulation
    d = 1
    # Size of on step (δt)
    step_size = 1
    # start position
    r = 0
    # number of steps
    max_steps = 100
    # list of performed steps
    steps = []
    # list of positions
    distances = []


    def boundary_condition(self, r_0, r_1):
        raise NotImplementedError("Should have implemented this")

    def boundary_position(self, r_0, r_1):
        raise NotImplementedError("Should have implemented this")

    def step(self):
        raise NotImplementedError("Should have implemented this")

    def keep_absorbed(self):
        raise NotImplementedError("Should have implemented this")

    def coordinate(self, r):
        raise NotImplementedError("Should have implemented this")

    def info_walk(self):
        self.steps = [0]
        self.distances = [self.coordinate(self.r)]
        step = 0
        absorbed = self.boundary_condition(self.r, self.r)
        while step < self.max_steps:
            step += 1
            r_old = numpy.copy(self.r)
            if not absorbed:

                self.r += self.step()
                absorbed = self.boundary_condition(r_old, self.r)
                if not absorbed:
                    self.steps.append(step)
                    self.distances.append(self.coordinate(self.r))
            if absorbed:
                self.r = self.boundary_position(r_old, self.r)
                keep_absorbed = int(self.keep_absorbed() / self.step_size)

                # Add start and end point of absorbed period.
                self.steps.append(step)
                self.distances.append(self.coordinate(self.r))
                step += keep_absorbed
                self.steps.append(step)
                self.distances.append(self.coordinate(self.r))

                # Now desorb
                r_old = self.boundary_position(r_old, self.r)
                step += 1
                while self.boundary_condition(r_old, self.r):
                    self.r = numpy.copy(r_old)
                    self.r += self.step()

                self.distances.append(self.coordinate(self.r))
                self.steps.append(step)
                absorbed = False

        return self.steps, self.distances