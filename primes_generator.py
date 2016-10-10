from Crypto.Hash import SHA256
import random


class PrimeGenerator(object):
    """
    Prime number generator according 2 FIPS 186
    """
    valid_pairs = [(1024, 160), (2048, 224), (2048, 256), (3072, 256)]
    VALID, INVALID = 1, 0

    @staticmethod
    def gcd(a, b):
        while a != 0:
            a, b = b % a, a
        return b

    def is_prime(self, x):
        if x == 2 or x == 3:
            return 1
        ans = 1
        q = x - 1
        while q % 2 == 0:
            q //= 2
        for i in range(100):
            a = random.randrange(2, x - 1)
            if self.gcd(a, x) != 1:
                return self.gcd(a, x)
            if pow(a, x - 1, x) != 1:
                return 0
            a = pow(a, q, x)

            if a != 1:
                while a != 1 and a != x - 1:
                    a = (a * a) % x
                if a == 1:
                    return 0
        return ans

    def __init__(self, seed_len):
        self.seed_len = seed_len
        self.seed = self.make_seed(seed_len)

    @staticmethod
    def make_seed(seed_len):
        return random.getrandbits(seed_len)

    @staticmethod
    def h(data):
        f = SHA256.new()
        f.update(str(data).encode())
        value = int(f.hexdigest(), base=16)
        return value

    def generate(self, L, N, seed_len):
        if tuple([L, N]) not in self.valid_pairs:
            return self.INVALID

        if seed_len < N:
            return self.INVALID

        out_len = 256
        n = L // out_len - 1
        b = L - 1 - (n * out_len)
        while True:
            q = 4
            while self.is_prime(q) != 1:
                domain_parameter_seed = self.make_seed(seed_len)
                U = self.h(domain_parameter_seed)
                q = 2**(N - 1) + U + 1 - (U % 2)

            offset = 1
            for counter in range(4*L):
                V = [self.h((domain_parameter_seed + offset + _) % 2**seed_len) for _ in range(n + 1)]
                W = 0
                for i in range(n):
                    W += V[i] * 2 ** (out_len * i)
                W += (V[n] % 2**b) * 2**(n * out_len)
                X = W + 2**(L - 1)
                c = X % (2 * q)
                p = X - (c - 1)
                if p >= 2**(L - 1):
                    if self.is_prime(p) == 1:
                        return tuple([p, q])
                offset += n + 1

if __name__ == "__main__":
    p = PrimeGenerator(10)
    res = p.generate(2048, 224, 1024)
    print (res[0] - 1) % res[1]
    print res[1] % res[0]
    print (p.is_prime(res[0]))
    print (p.is_prime(res[1]))
