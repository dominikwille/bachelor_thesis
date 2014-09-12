import matplotlib.pyplot as plt
import numpy
import math


def nCr(n,rs):
    f = math.factorial
    vals = []
    for r in rs:
        r = int(r)
        vals.append(f(n) / f(r) / f(n-r))
    return vals

n = 1000
epsilon = 3.0
X = n




def p_ana(x):
    k = 0.5 * (n + x / epsilon)
    return numpy.array(nCr(n, k)) * 2.0**(-n)

def p_test(x):
    # return ((n/(2*numpy.pi*k*(n-k)))**0.5)*(n**n/((k**k) * (n-k)**(n-k))) * 2**(-n)
    a = (n/(0.5*numpy.pi*(n+x/epsilon)*(n-x/epsilon)))**0.5
    # a = 1 / epsilon / (2*numpy.pi*n)**0.5
    a = (2/numpy.pi/n) ** 0.5

    b = numpy.exp(-0.5*((n+x/epsilon)*numpy.log(1+x/epsilon/n) + (n-x/epsilon)*numpy.log(1-x/epsilon/n)))
    b = numpy.exp(
        -0.5*(n+x/epsilon)*(x/epsilon/n - x**2/2/epsilon**2/n**2)
        -0.5*(n-x/epsilon)*(- x/epsilon/n - x**2/2/epsilon**2/n**2)
    )
    # b = numpy.exp(-x**2/epsilon**2/n)

    return a * b

def p_app(x):
    k = 0.5 * (n + x / epsilon)
    return ((2/numpy.pi/n)**0.5)*numpy.exp(-(x/epsilon)**2/(2*n))

x = numpy.arange(-X, X+1, epsilon)
plt.plot(x, p_ana(x), 'r')
plt.plot(x, p_app(x), 'g')
plt.plot(x, p_test(x), 'b')
plt.show()