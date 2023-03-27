import random
import argparse
import sys


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def generate_prime(digits):
    while True:
        num = random.randint(10 ** (digits - 1), (10 ** digits) - 1)
        if is_prime(num):
            return num


def find_modular_inverse(d, m):
    gcd, x, y = extended_euclidean_algorithm(d, m)
    if gcd != 1:
        return None
    return x % m


def extended_euclidean_algorithm(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_euclidean_algorithm(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def pow_mod(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result


def generate_keys():
    p = generate_prime(9)
    q = generate_prime(9)
    while p == q:
        p = generate_prime(9)
        q = generate_prime(9)
    n = p * q
    m = (p - 1) * (q - 1)
    e = random.randrange(1, m)
    g = gcd(e, m)
    while g != 1:
        e = random.randrange(1, m)
        g = gcd(e, m)
    d = find_modular_inverse(e, m)
    return f'{d}-{n}', f'{e}-{n}'


def encrypt(file, file_to, key):
    key = list(map(int, key.split('-')))
    to = open(file_to, "a+")
    with open(file, "rb") as f:
        while byte := f.read(1):
            to.write(str(pow_mod(int.from_bytes(byte, "little"), key[0], key[1])) + "\n")


def decrypt(file, file_to, key):
    key = list(map(int, key.split('-')))
    to = open(file_to, "wb")
    with open(file, "r") as f:
        data = f.readlines()
        for line in data:
            to.write(pow_mod(int(line), key[0], key[1]).to_bytes(1, 'little'))


parser = argparse.ArgumentParser(description='RSA')
parser.add_argument('command', choices=['encrypt', 'decrypt', 'generate'], help='Command')
parser.add_argument('-k', '--key', type=str, help='Key')
parser.add_argument('-i', '--input', type=str, help='Input File',
                    required=('encrypt' in sys.argv or 'decrypt' in sys.argv))
parser.add_argument('-o', '--output', type=str, help='Output File',
                    required=('encrypt' in sys.argv or 'decrypt' in sys.argv))
args = parser.parse_args()

if args.command == 'encrypt':
    private, public = '', ''
    if args.key is not None:
        private = args.key
    else:
        private, public = generate_keys()
    encrypt(args.input, args.output, private)
    if args.key is None:
        print(f'public key: {public}')
        print(f'private key: {private}')

elif args.command == 'decrypt':
    private, public = '', ''
    if args.key is not None:
        public = args.key
    else:
        private, public = generate_keys()
    decrypt(args.input, args.output, public)
    if args.key is None:
        print(f'public key: {public}')
        print(f'private key: {private}')
else:
    private, public = generate_keys()
    print(f'public key: {public}')
    print(f'private key: {private}')
