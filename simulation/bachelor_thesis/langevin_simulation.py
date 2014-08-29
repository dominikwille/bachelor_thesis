#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# @author Dominik Wille

import numpy
import os
import csv
import matplotlib.pyplot as plt
import random

# This defines the dimension of the simulation
D = 1
# TODO: Think over this....
step_size = 1

# This function simulates a radom walk of the defined number of steps.
def info_walk(
        r_0, max_steps,
        boundary_condition_callback,
        boundary_position_callback,
        step_callback,
        keep_absorbed_callback,
        coordinate_callback):

    steps = [0]
    distances = [coordinate_callback(r_0)]
    r = r_0
    step = 0
    while step < max_steps:
        step += 1
        r_old = numpy.copy(r)
        r += step_callback()

        if boundary_condition_callback(r_old, r):
            r = boundary_position_callback(r_old, r)

            keep_absorbed = int(keep_absorbed_callback() / step_size)

            steps.append(step)
            distances.append(coordinate_callback(r))

            step += keep_absorbed
            steps.append(step)
            distances.append(coordinate_callback(r))
        else:
            steps.append(step)
            distances.append(coordinate_callback(r))

    return steps, distances

def simple_step():
    mean = 0
    variance = 1

    r = []
    i = 0
    while i < D:
        i += 1
        r.append(random.gauss(mean, variance))

    return numpy.array(r)


