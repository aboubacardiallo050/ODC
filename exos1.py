import math

# 2. OOP METHOD
import math


def f(x): return x / (x.__pow__(2) + 1)
def g(x): return math.atan(x)
def L(N): return range(-N, N + 1)


def R(i): return sum([(abs(f(x) - g(x))) ** 2 for x in L(i)])
