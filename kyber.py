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
        s = discrete_gaussian(self) #kx1
        e = discrete_gaussian(self) #kx1

        a1 = [] #kxk
        a0 = [] #kx1
        for i in range(self.k):
            a1.append(discrete_gaussian(self))
        
        for i in range(self.k): #WILL BE REPLACED BY API CALL
            coeffs = []
            for j in range(self.k):
                coeffs.append(a1[i][j]*s[j])

            coeffs[i] += e[i]
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

        m = Rq(m.poly.coeffs, self.q)
 
        u = [] # kx1
        v = [] # 1x1

        for i in range(self.k):
            for j in range(self.k):
                u.append(a1[j][i]*e[0][j])
            u[i] += e[1][i]
            v.append(a0[i]*e[0][i])
        v[0] += e[2][0] + m


        return (u,v)

    def decrypt(self, c, s):
        '''
        # Args:
            c: ciphertext (c0, c1, ..., ck)
            s: secret key
        '''
        u,v = c
        m = []

        for i in range(self.k):
            m.append(s[i]*u[i])
        
        m[0] = v[0] - m[0]

        return m[0]

def discrete_gaussian(self):
    s = []
    for _ in range(self.k):

        tuple_coeffs = CALLS.callGAUSSAMPLER() #will call the request_queue
        coeffs = []
        for num in tuple_coeffs:
            coeffs.append(num)
        s.append(Rq(coeffs,self.q))

    return s
