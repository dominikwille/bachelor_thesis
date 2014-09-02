#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import numpy
import random

# This defines the dimension of the simulation
D = 1
# TODO: Think over this....
step_size = 1

# This function simulates a radom walk of the defined number of steps.
def info_walk(
        r_0,
        max_steps,
        boundary_condition_callback,
        boundary_position_callback,
        step_callback,
        keep_absorbed_callback,
        coordinate_callback):

    steps = [0]
    distances = [coordinate_callback(r_0)]
    r = r_0
    step = 0
    absorbed = boundary_condition_callback(r_0, r_0)
    while step < max_steps:
        step += 1
        r_old = numpy.copy(r)
        if not absorbed:

            r += step_callback()
            absorbed = boundary_condition_callback(r_old, r)
            if not absorbed:
                steps.append(step)
                distances.append(coordinate_callback(r))
        if absorbed:
            r = boundary_position_callback(r_old, r)
            keep_absorbed = int(keep_absorbed_callback() / step_size)

            # Add start and end point of absorbed period.
            steps.append(step)
            distances.append(coordinate_callback(r))
            step += keep_absorbed
            steps.append(step)
            distances.append(coordinate_callback(r))

            # Now desorb
            r_old = boundary_position_callback(r_old, r)
            step += 1
            while boundary_condition_callback(r_old, r):
                r = numpy.copy(r_old)
                r += step_callback()

            distances.append(coordinate_callback(r))
            steps.append(step)
            absorbed = False

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


