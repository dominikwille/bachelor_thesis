from langevin_simulation import *

def P():
    tao = 0.03
    t = random.expovariate(tao)
    return t

def plate_position(r_0, r_1):
    plate_0 = 5.0
    plate_1 = -5.0
    if (r_0 < plate_0 and r_1 > plate_0) or (r_1 < plate_0 and r_0 > plate_0):
        plate = plate_0
    elif (r_0 < plate_1 and r_1 > plate_1) or (r_1 < plate_1 and r_0 > plate_1):
        plate = plate_1
    else:
        plate = 0
    return numpy.array([plate])

def plate_boundary(r_0, r_1):
    return plate_position(r_0, r_1) != 0

def first_component(r):
    return r[0]

r_0 = numpy.array([0.0])
max_steps = 1000

x, y = info_walk(r_0, max_steps, plate_boundary, plate_position, simple_step, P, first_component)

plt.plot(x, y)
plt.ylim([-20, 20])
plt.show()