import numpy as np
from .Rq import Rq
from .utils import crange
import CALLS


class KYBER:
    def __init__(self, n, p, t, k, std,q):
        assert np.log2(n) == int(np.log2(n))
        self.n = n
        self.p = p
        self.t = t
        self.k = k
        self.q = q
        self.std = std

    def generate_keys(self):
        s = discrete_gaussian() #kx1
        e = discrete_gaussian() #kx1

        a1 = [] #kxk
        a0 = [] #kx1
        for i in range(self.k):
            temp = []
            for i in range(self.k):
                a1.append(discrete_gaussian())
        
        for i in range(self.k): #WILL BE REPLACED BY API CALL
            coeffs = []
            for j in range(self.k):
                coeffs.append(a1[i][j]*s[j])
            a0.append(Rq(coeffs,self.q))

        return (s, (a0, a1))  # (secret, public)

    def encrypt(self, m, a):
        '''
        # Args:
            m: plaintext (mod t)
            a: public key (a0, a1)
        '''
        a0, a1 = a
        e = [discrete_gaussian(self)
             for _ in range(3)]

        m = Rq(m.poly.coeffs, self.p)

        return (m + a0 * e[0] + self.t * e[2], a1 * e[0] + self.t * e[1])

    def decrypt(self, c, s):
        '''
        # Args:
            c: ciphertext (c0, c1, ..., ck)
            s: secret key
        '''
        c = [ci * s**i for i, ci in enumerate(c)]

        m = c[0]
        for i in range(1, len(c)):
            m += c[i]

        m = Rq(m.poly.coeffs, self.t)

        return m

    def add(self, c0, c1):
        '''
        # Args:
            c0: ciphertext (c0, c1, ..., ck)
            c1: ciphertext (c'0, c'1, ..., c'k')
        '''
        c = ()

        k0 = len(c0)  # not necessary to compute (len - 1)
        k1 = len(c1)

        if k0 > k1:
            (c0, c1) = (c1, c0)  # c0 is always shorter

        for _ in range(abs(k0 - k1)):
            c0 += (Rq([0], self.p),)  # add 0 to shorter ciphertext

        for i in range(len(c0)):
            c += (c0[i] + c1[i],)

        return c

    def mul(self, c0, c1):
        '''
        # Args:
            c0: ciphertext (c0, c1, ..., ck)
            c1: ciphertext (c'0, c'1, ..., c'k')
        '''
        c = ()

        k0 = len(c0) - 1
        k1 = len(c1) - 1

        for _ in range(k1):
            c0 += (Rq([0], self.p),)

        for _ in range(k0):
            c1 += (Rq([0], self.p),)

        for i in range(k0 + k1 + 1):
            _c = Rq([0], self.p)
            for j in range(i+1):
                _c += c0[j] * c1[i-j]
            c += (_c,)

        return c


def discrete_gaussian(self):
    s = []
    for i in range(self.k):
        tuple_coeffs = CALLS.callGAUSSAMPLER()
        coeffs = []
        for num in tuple_coeffs:
            coeffs.append(num)
        coeffs = coeffs[1 : ]
    s.append(Rq(coeffs,self.q))
    return s
