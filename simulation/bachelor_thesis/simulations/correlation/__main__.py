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
    D = 0.2
    # Size of on step - 1/resolution (δt)
    step_size = 0.1
    # Parameter of the exponential decaying desorbtion probability
    tao = 10.0 * step_size
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
        mean = 0

        r = []
        i = 0
        while i < self.d:
            i += 1
            r.append(random.gauss(mean, self.variance))

        return numpy.array(r)
        # return numpy.array([random.choice([1.0, -1.0])])

    def keep_absorbed(self):
        t = random.expovariate(1.0 / self.tao)
        return t

    def coordinate(self, r):
        if self.absorbed:
            c = 1
        else:
            c = 0
        return c

# num = 1
# max_steps = 10000000
# # correlation = numpy.array([0.0]*max_steps)
# correlation_x_min = 0
# correlation_x_max = 300
# correlation_precision = 100000
# correlation = numpy.array([0.0]*(correlation_x_max - correlation_x_min))
# x = numpy.array(range(correlation_x_min, correlation_x_max))
#
#
# # for j in range(100):
# #     print j
# #     for i in range(num):
# #         test = Plates1dNoCrossing()
# #         test.absorbed = True
# #         test.max_steps = max_steps
# #         test.r = numpy.array([-10.0])
# #         x, y = test.info_walk()
# #         correlation += numpy.array(y)
# # correlation /= float(num*100)
#
# test = Plates1dNoCrossing()
# test.absorbed = True
# test.max_steps = max_steps
# test.r = numpy.array([-10.0])
# steps, y = test.info_walk()
#
# for i in range(correlation_x_max - correlation_x_min):
#     print i
#     j = 0
#     j_index = 0
#     while j < correlation_precision:
#         if y[j_index] == 1:
#             j += 1
#             if y[j_index + i + correlation_x_min] == 1:
#                 correlation[i] += 1
#         j_index +=1
#
# correlation /= float(correlation_precision)

import csv

c_aa = []
c_ab = []
xdata = []
i = 0.0
with open('data/p1.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        xdata.append(i)
        c_aa.append(float(row[0]))
        c_ab.append(float(row[1]))
        i += 1.0

from scipy.optimize import curve_fit

def func0(x_, a, b, c, d, f, g, h):
    return a * numpy.exp(x_ * b) + c * numpy.exp(x_ * d) + f * numpy.exp(x_ * g) + h

def func1(x_, j, k, l):
    return j * numpy.exp(- x_ / k) + l
# popt0 = [ 0.07712867,  0.00204063,  0.55760507,  0.10309138,  0.30010113,  0.01889753,  0.02938739]
# popt0 = [ 0.25477613,  0.10796093,  0.28181761,  0.01268437,  0.28845823,  0.001656, 0.1156842 ]
def expect(x_):
    return numpy.exp(-x_)

popt0, pcov0 = curve_fit(func0, xdata, c_aa)
popt1, pcov1 = curve_fit(func1, xdata, c_ab)

print popt0
print popt1

# p0, = plt.plot(xdata, c_aa)
# p1, = plt.plot(xdata, c_ab)
# p2, = plt.plot(xdata, func0(numpy.array(xdata), *popt0))
# p3, = plt.plot(xdata, func1(numpy.array(xdata), *popt1))
# plt.legend([p0, p1, p2, p3], ['$C_{AA}$', '$C_{AB}$', '$C_{AA}$ fit', '$C_{AB}$ fit'], loc=2)
# plt.xlabel('Step')
# plt.ylabel('Probability')
# plt.ylim([0, 1])
# plt.show()

step_size = 0.1
tau = 1.0
k = p = 1000
D = 0.1
H = 1.0

def laplace(w_, a, b, c, d, f, g, h):
    return a / (b+w_) / step_size + c / (d+w_) /step_size + f / (g+w_) + h / w_ / step_size

def laplace2(w_, xdata):
    val = []
    xdata = numpy.array(xdata) * step_size
    for w_i in w_:
        A = numpy.matrix([numpy.exp(-w_i * xdata)])
        B = numpy.matrix([c_aa]).T
        vali = A * B * step_size
        val.append(vali[0, 0])
    return val


def roland(w_, tau, k, D, H):
    data = [tau, k, D, H]
    return Q(w_, data) * (1-P(w_, data)) * J_BB(w_, data) / (
        (1-P(w_, data) * J_AA(w_, data)) * (1- P(w_, data) * J_BB(w_, data)) - P(w_, data) * J_AB(w_, data) * J_BA(w_, data)
    )

def Q(w_, data):
    tau = data[0]
    return tau / (1.0 + tau * w_)

def P(w_, data):
    tau = data[0]
    return 1.0 / (1.0 + tau * w_)

def J_BB(w_, data):
    return J_AA(w_, data)

def J_AA(w_, data):
    k = data[1]
    H = data[3]
    D = data[2]
    return k * (1-k+numpy.exp(2 * H * (w_ / D)**0.5) * (1+k)) / (
        numpy.exp(2 * H * (w_ / D)**0.5) * (1+k)**2 - (1-k)**2
    )

def J_BA(w_, data):
    return J_AB(w_, data)

def J_AB(w_, data):
    k = data[1]
    H = data[3]
    D = data[2]
    return 2 * numpy.exp(H * (w_ / D)**0.5) * k / (
        numpy.exp(2 * H * (w_ / D)**0.5) * (1+k)**2 - (1-k)**2
    )

def lim(w_, tau, k, D, H):
    return 1 / (w_ - 1 / (tau**2 * w_**2 * k**2 * numpy.sinh(H * (w_ / D)**0.5)))


w = numpy.arange(0.0001, 10.0, 0.01)

popt2, pcov2 = curve_fit(roland, w, laplace2(w, xdata))

print popt2

p0, = plt.plot(w, laplace2(w, xdata))
# p1, = plt.plot(w, laplace(w, *popt0))
p1, = plt.plot(w, roland(w, tau, k, D, H))
# p2, = plt.plot(w, roland(w+0.09, tau, k, D, H) +0.09)
# p2, = plt.plot(w, lim(w, tau, k, D, H))
# plt.legend([p0, p1, p2], ['laplace transformed data', 'analytic', 'analytic limit'], loc=2)
plt.legend([p0, p1], ['laplace transformed data', 'analytic'], loc=2)
plt.xlabel('Step')
plt.ylabel('Probability')
plt.ylim([0, 10])
plt.show()