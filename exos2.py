# 5.
import random


class DataTrans:
    def __init__(self, S, n):
        S = 2
        n = 3
        self.N = lambda: [random.randint(0, 100) for i in range(S)]
        self.D = [self.N() for i in range(n)]
        self.f = lambda x: (x ** 3) + ((3) * (x**2)) - 5

    def findmin(self, arr):
        value = arr[0]
        for i in range(1, len(arr)):
            if arr[i] < value:
                value = arr[i]
        return value

    def findmax(self, arr):
        value = arr[0]
        for i in range(1, len(arr)):
            if arr[i] > value:
                value = arr[i]
        return value

    def EACH_MIN_IN_D(self):
        return [self.findmin(x) for x in self.D]

    def EACH_MAX_IN_D(self):
        return [self.findmax(x) for x in self.D]

    def GLOBAL_MIN(self):
        return self.findmin(self.EACH_MIN_IN_D())

    def GLOBAL_MAX(self):
        return self.findmax(self.EACH_MAX_IN_D())

    def f_d(self):
        D_PRIME = [x for x in self.D]
        for i in range(len(D_PRIME)):
            element = D_PRIME[i]
            # map element and replace with new value
            D_PRIME[i] = list(map(lambda x: self.f(x), element))
        return D_PRIME
